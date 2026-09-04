# Luna reply -- Task904 / R07 physical-state manifest contract v2

Implemented exactly the four authorized v2 files.  The repair is limited to
the rho2 manifest ABI, corresponding fixtures/mutation controls, and the
versioned workflow/source labels.  Physical elimination, reverse insertion,
state/output/launch production ABIs, parent identities, caps, and claim
boundaries remain unchanged.

## Failure being repaired

Run `33889253581/1`, job `101076608011`, head
`1a7bbdeb5be0b5c80fcf9bec2c72940d972f186a`, failed only with:

```text
{"status":"REJECTED","error":"rho2_manifest_shape","verified":false}
```

The unchecked candidate was artifact `9943198098`,
`d972-r07-grade2-physical-state-separator-v1-candidate-unchecked-33889253581-1`,
`106041813` bytes, digest
`sha256:4b9b6cc4581b7f222dcd4783593b3d5eab1c558c2088315831a4d08b92002f87`.
This was a wiring failure and no Grade-2 result was inferred or reused.

## v2 semantic delta

Both independent readers now authenticate the raw live manifest size/SHA
(`26047`, `55c42f06e70b2150d324ed8649fe4af0e6db1bf0e87e315db570d1fa80f61488`)
before JSON field interpretation and require canonical ASCII JSON.  They then
require the production dictionary contract:

```text
dimensions={lower:32260,packed_rho2:12096,top:48384}
lower_all_zero=true
rho2={packed_sha256, dense_sha256, packing_roundtrip=true}
files={lower_dense,path_signatures,rho2_dense,rho2_packed,roots,
       signature_buckets,target_dense}
```

Each role receipt is shape-checked and normalized by its `file` value only
after the dictionary and seven-role set are proven; all seven frozen payload
receipts, exact roster, verdict, acquisition, packed/dense equality, and
32,260-byte all-zero lower payload remain checked.  Producer and checker use
separate implementations.  The old v1 list/top-level-hash shape is a named
rejecting regression in both selftests; production-shaped dictionary fixtures
are accepted and still cover MEMBER, Separator, nonmonotone pivots,
stop/resume, and the prior mutation suite.

The accepted parent launch fields remain the frozen connection v6/checker v7
identities (not the v2 script receipts).  Only workflow source authentication
and invoked script paths use v2.  Production state, terminal, checker-result,
and launch schemas remain v1; runner selftest schemas and workflow-input
receipt are v2.

## Exact source receipts

All files are BOM-free, CR-free, and final-LF terminated.

| file | bytes | LF | SHA-256 |
|---|---:|---:|---|
| `search/d972_r07_grade2_physical_state_separator_v2.py` | 79,122 | 1,462 | `b068c9f3be153c5381f583b4a82448d5680777ce71ccb5250c2bbb972c8cff2e` |
| `search/check_d972_r07_grade2_physical_state_separator_v2.py` | 60,997 | 780 | `bb5d0c0a51408a65c3200b552e6a1eac2f832abeeca8e19fcce64d570f0967f6` |
| `.github/workflows/d972-r07-grade2-physical-state-separator-v2.yml` | 20,126 | 405 | `e7529e03f0125ae0d6b28f1fb817757d61d1f12dcb48ad929052fe7a1e81b6d7` |

## Workflow boundary

The v2 workflow uses `ubuntu-24.04`, Python 3.13, pinned
`numpy==2.5.1`, fresh `resume=false` runner-temp roots, accepted stager v4,
30-minute producer/checker caps inside a 75-minute job, 1-second completion
polling with approximately 60-second progress emission, and compression
level 0.  The unchecked candidate artifact is uploaded after the checker
under `always()`; final candidate publication requires both named steps to
succeed.  Final labels are v2 and say candidate, never verified.  The sole
inert marker is:

```text
[task904-r07-physical-state-separator-v2]
```

## Bounded checks and exact-parent smoke

The final v2 sources passed:

```text
py_compile producer/checker: PASS
producer --selftest: PASS
checker --selftest: PASS (old v1 list rejected; all prior mutations rejected)
producer --benchmark: PASS, status=BOUNDED_ONLY
YAML/static: PASS (one job, one marker, 5 API calls, v2 source hashes,
  1-second polling, approximately-60-second progress, caps 30/30/75,
  compression-level: 0 twice)
```

The benchmark retained `offers=6`, `physical_rank=3`, `physical_reductions=2`,
`target_reductions=1`, `reverse_substitution=3`, and live bound `915981`.
The exact-parent smoke staged the v17 payload through accepted stager v4 with
manifest `26047` bytes and staged output `75319124` bytes.  Producer and
checker live target readers independently returned:

```text
producer_live_target_reader=PASS bytes=12096
checker_live_target_reader=PASS bytes=12096
```

No physical state was rebuilt, no GHA/Git/credential operation was used, and
no actual Grade-2 decision is declared.

```text
ACTUAL_CONNECTION_STATE=false
GRADE2_MEMBER/NONMEMBER=NOT_DECIDED
A0/COMMON/COFINAL_LIFT/FAKE/IHARA=NOT_DECLARED
cross_checked=false
verified=false
```

R07_PHYSICAL_STATE_MANIFEST_CONTRACT_V2_READY_FOR_SOL_AUDIT
