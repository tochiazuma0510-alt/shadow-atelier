# Luna Task612: external-owner v10 strict compile/interop GHA wrapper

Role: Luna implementation. Read in full:

1. `sol/sol_reply_610_audit_r07_external_owner_worker_v10.md`
2. `sol/luna_task_603_r07_external_owner_worker_v10.md`
3. `search/d972_external_owner_gf3_worker_v10.c`
4. `search/d972_external_owner_gf3_worker_v10.py`
5. `search/check_d972_external_owner_gf3_worker_v10.py`
6. `sol/luna_reply_603_r07_external_owner_worker_v10.md`

Create only:

1. `.github/workflows/d972-r07-external-owner-v10-interop-v1.yml`
2. `sol/luna_reply_612_r07_external_owner_v10_gha_compile_interop_v1.md`

Do not edit the audited v10 trio, proofs, v220 or any other file. Do not
commit, push, dispatch, run GHA or run production.

## Exact finite workflow

Implement exactly the one bounded compiler-present campaign authorized by
Task610. Use `ubuntu-latest`, Python 3.13, a 15-minute job timeout, no matrix,
no sharding and no production input. Pin and assert the three audited source
hashes before execution:

```text
worker C       8938bcdad693553266aeb08cfe023548fcb8d5965683157e60df564ea16681bd
owner Python   3b6441063348987d101a9dc8ac019b2dcc85dee983f77342b821db710c00a16c
checker        34016ce93096cfdc1e28735468a624016c6e53be6b39a1002adc1f07b9d44f63
```

Run only:

```text
python -B search/check_d972_external_owner_gf3_worker_v10.py
```

Capture its complete log and final JSON report. Add a small inline Python
assertion which parses the report and enforces every numbered item 1--9 in
Task610's `Exact bounded GHA gate`, including compiler present, strict compile
fields, exact five stream hashes, three cap gates, 87 partial headers, malformed
and noncanonical terminals, allocation failpoint separation, fragmentation,
stall/short poison behavior, hard-kill provisional IDs/offsets, four clean
mutation controls with the exact rejection names, and final
`interoperability=PASS`. Exit zero from the checker alone is insufficient.

The workflow must be launchable on its first marker push. Provide a narrow
push trigger for branch `sol/r07-explicit-lift-20260825` and require commit
message marker `[fire-external-owner-v10-interop]`; also allow
`workflow_dispatch`. Upload the raw log and parsed JSON as one artifact even
on failure. Record run ID/head SHA later in the root reply, not as a fabricated
constant in this implementation reply.

Use no optional fuzzing, benchmarks, production adapter, grade-one rank-8059
mode or additional package installation. This wrapper is a finite compiler and
wire-interop gate only.

Run only local YAML/text sanity checks which require no compiler. Report exact
byte counts/SHA-256 values and readiness honestly in the designated reply.

```text
PRODUCTION: false
verified: false
```
