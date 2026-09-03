# Luna Task745 -- grade-two maps producer-v3/checker-v4 GHA wrapper

```text
RESULT=COMPLETE
REAL_GHA_RUN=NOT_RUN
verified=false
```

Created only the commissioned v4 workflow and this reply.  The workflow is
`workflow_dispatch`-only with no job-level fire condition.  It keeps producer
v3 unchanged, including its v3 schema and
`R07_GRADE2_FORWARD_ADJOINT_MAPS_V3_CANDIDATE` marker, and binds checker v4
with its exact V4 PASS marker.  The 40-table sparse build, roster/EOF
authentication, independent checker, false claim flags, bounded timeouts and
logs remain serial.  Temporary paths, artifact names, workflow receipt name,
and workflow receipt schema are v4.  No retry, parallelism, cache, dependency,
new computation, actual `--emit`/`--check`, GHA, or git operation was run.

The v490 proof, Task741 reply, and Task744 audit are preflight-authenticated
by exact byte size, final LF, and SHA-256.  The exact audit lines
`VERDICT=PASS_GRADE2_MAPS_CHECKER_V4_SAFE_FOR_GHA` and
`SAFE_TO_DISPATCH_GHA=yes` are required.

## Exact receipts

| path | bytes | LF | final LF | SHA-256 |
|---|---:|---:|:---:|---|
| `.github/workflows/d972-r07-grade2-maps-v4.yml` | `11011` | `216` | yes | `166bba8584b76bd5990821ac04676cbdd8a18045773d7c69cebccb56924c6720` |
| `search/d972_r07_grade2_forward_adjoint_maps_v3.py` | `46179` | `989` | yes | `7d6243901ef34b5c00e56e7be517beb8775fe83aedd277b23c4ed4fb29a72b84` |
| `search/check_d972_r07_grade2_forward_adjoint_maps_v4.py` | `49643` | `1013` | yes | `7ba94ee884db49bbe42d11a84228a6bdf7c88a3918407928af90c71b65fe4a29` |
| `sol/proof_r07_grade2_maps_coverage_receipt_schema_v490.md` | `1412` | `38` | yes | `e322c8e5546fc51e2d65e1fc85fa988bd92ce4475b3992aaf505fdfc668f48e4` |
| `sol/luna_reply_741_r07_grade2_maps_checker_receipt_v4.md` | `2792` | `76` | yes | `cd73e4db862f5fbbc7972232ade9f560d607f203ee0862ff13ee4e072937b3f1` |
| `sol/sol_reply_744_audit_r07_grade2_maps_checker_v4.md` | `9111` | `199` | yes | `b1e1a6fc307df0d417fcd718efa324009204081ed58d4fe7dbe44e6934a11a7c` |

The reply's own digest is supplied post-seal rather than embedded, avoiding a
self-referential receipt.

## Bounded checks

```text
python -B search/d972_r07_grade2_forward_adjoint_maps_v3.py --selftest
exit 0; fixture=PASS; ACTUAL_MAP_BUILD=DEFERRED_TO_GHA; GRADE2_DECISION=NOT_RUN

python -B search/check_d972_r07_grade2_forward_adjoint_maps_v4.py --selftest
exit 0; fixture=PASS; fixture_rejection_count=13; verified=false
```

YAML parsing passed; the only event is `workflow_dispatch` and the job `if`
is absent.  No map artifact or build-scale receipt was produced.
