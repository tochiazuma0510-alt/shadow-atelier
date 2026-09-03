# Luna Reply 732 — inert GHA wrapper for grade-two maps v2

## Result

`DONE`. The workflow remains literally inert. No workflow was armed or dispatched; no real map artifact, git operation, grade-two decision, A0, COMMON, compatible cofinal lift, fake, Ihara, or Lean verification claim was produced.

## Output receipt

| file | bytes | LF | CRLF | final LF | SHA-256 |
|---|---:|---:|---:|---|---|
| `.github/workflows/d972-r07-grade2-maps-v2.yml` | 10,483 | 208 | 0 | yes | `8a4cc6f6ff075443ab8cfec6c88e11558304457874e0becc33fa73049352ecfb` |
| `sol/luna_reply_732_r07_grade2_maps_v2_gha.md` | sealed reply | sealed reply | 0 | yes | supplied externally after sealing |

## Frozen preflight

The job fails before execution unless all three inputs match their path, byte count, final LF, and SHA-256:

```text
producer  44667 bytes  fdcb9a8ca9804179f350500c02203cdde550498b5cc5912ff1b0bde1d92e4d84
checker   48459 bytes  e388300c88de674d6e4550a7f20a40031488e724e40e73cdc89189b472ae61f0
audit     10488 bytes  c63f7e1ee7289452ed4db8f22f3a1e1e0bf888fb7129fc09e51c7abf181bca9d
```

It also requires Python `3.13` and the exact audit lines
`PASS_GRADE2_MAPS_V2_SAFE_FOR_GHA` and `SAFE_TO_DISPATCH_GHA=yes`.

Pinned actions copied from accepted recent R07 workflows:

```text
actions/checkout@11d5960a326750d5838078e36cf38b85af677262
actions/setup-python@8d9ed9ac5c53483de85588cdf95a591a75ab9f55
actions/upload-artifact@65462800fd760344b1a7b4382951275a0abb4808
```

## Job policy

- trigger: `workflow_dispatch` only;
- literal job guard: `if: ${{ false }}`;
- runner: `ubuntu-24.04`;
- overall timeout: 75 minutes;
- producer/checker selftests: 3 minutes each;
- actual producer: 30 minutes, TERM then 30-second kill-after;
- independent checker: separate 30 minutes, TERM then 30-second kill-after;
- `set -euo pipefail`, Python unbuffered output, and `tee` preserve the actual pipeline exit status;
- bytecode cache, artifact, checker result, workflow receipt, and logs are fresh paths under `$RUNNER_TEMP` only;
- producer terminal, marker file, manifest, exact 40-table/42-file roster, and every table's terminal EOF record are required before checker invocation;
- checker exit zero, PASS marker, exact 40-table authentication, entry-count agreement, and exact false claim boundary are required;
- `Traceback`, `UNKNOWN_`, `HARD_STOP`, or `ERROR` in bounded/real logs rejects;
- timeout or failure is a failed job, never a mathematical result;
- the success-only upload contains the map directory, checker JSON, compact workflow receipt, and bounded logs as one artifact;
- artifact name: `d972-r07-grade2-maps-v2-${{ github.run_id }}-${{ github.run_attempt }}`;
- retention: 30 days; missing upload inputs are an error; compression level 0;
- no checkpoint scheme or unrelated P1/A0/connection/CEGAR work is present.

The compact receipt binds run id/attempt, event commit SHA, executable hashes and sizes, manifest/checker-result hashes, table/map/entry counts, producer/checker reported elapsed time, and `/usr/bin/time` elapsed/peak-RSS measurements.

## Static checks

Performed without running the job:

```text
YAML safe parse: PASS
workflow_dispatch present: PASS
literal inert guard present: PASS
overall/process timeouts present: PASS
all three frozen SHA pins present: PASS
both authorization markers present: PASS
all real output paths use RUNNER_TEMP: PASS
exact producer/checker markers present: PASS
upload step guarded by success(): PASS
retention-days=30: PASS
```

Only the workflow and this reply were created. The two Python executables and every other workflow remain unchanged.

```text
WORKFLOW_INERT=true
ACTUAL_MAP_BUILD=NOT_RUN
GRADE2_DECISION=NOT_RUN
verified=false
```

`R07_GRADE2_MAPS_V2_GHA_WRAPPER_INERT`
