# Luna Task751 -- P1 checker-only GHA v1

Role: Luna.  Build only the bounded checker-only workflow authorized by
Task750.  Do not rerun producer prepare/blocks/join, edit mathematics or
checker code, run real artifacts, use git, push, or dispatch.

Read completely:

- `.github/workflows/d972-r07-p1-componentwise-semantic-v2.yml`
- `sol/proof_r07_p1_checker_state_head_schema_repair_v493.md`
- `sol/luna_reply_749_r07_p1_checker_state_head_v4.md`
- `sol/sol_reply_750_audit_r07_p1_checker_state_head_v4.md`
- `crosscheck/check_d972_r07_grade2_p1_componentwise_semantics_v4.py`

Create only:

- `.github/workflows/d972-r07-p1-semantic-checker-only-v1.yml`
- `sol/luna_reply_751_r07_p1_checker_only_gha_v1.md`

## Immutable producer input

Reuse, without regeneration:

```text
producer run/attempt 33814881435/1
producer head        15778e83c52941040ef9d4289ab76d897ee30ebc
artifact id          9916479231
artifact name        task729-p1-semantic-six-receipts-33814881435-1
archive bytes        8412
artifact digest      sha256:91281261a272e6ff48104a579a86e9cb300fc1543eaad1321b609e6d83564245
producer v5 SHA      dc5931c3fd3ad5d1a947346599824b02ad1d7b5f699361c05f1f051076dcbdcf
```

The artifact contains exactly the original prepare, block-0--3 and join
receipts.  Authenticate its GitHub metadata (id/name/bytes/digest/run/head),
download it from the exact run, require exactly those six canonical files,
and let checker-v4 compare their raw digests.

Reuse all five immutable Task554 parent artifact identities/digests and exact
download layout from workflow v2.  Do not silently switch parent run or name.

## Workflow

Use a new push-only workflow on branch `sol/r07-explicit-lift-20260825`, path
to itself, and require `[fire-r07-p1-checker-only-v1]` on every job.  No
`workflow_dispatch`.  Pin checkout/setup-python/download/upload action SHAs
from v2 and NumPy `2.5.1`.

Authenticate exact bytes/LF/final-LF for checker-v4, producer-v5 provenance,
v493, Task749 reply and Task750 reply.  Require Task750's two exact PASS
tokens.  Compile and run checker-v4 selftest before downloading large inputs.

Run only checker-v4 `--check` with the same five parent-root and six positional
receipt arguments as v2.  Preserve the 345-minute process timeout, 360-minute
job timeout, 12,000,000 KiB virtual-memory guard, single BLAS threads, time/RSS
log and `UNKNOWN_RESOURCE` routing.  Require the existing audited checker
marker

```text
R07_GRADE2_P1_COMPONENTWISE_INDEPENDENT_CHECKER_V1_PASS
```

and a canonical result with exact source ancestry, ranks/counts, producer-v5
SHA, six raw receipt digests, `independent_checker=true`, and every downstream
claim false.  Do not invent a new arithmetic marker; a workflow-only release
label may be clearly marked non-authoritative.

After success, create a canonical workflow receipt binding current
run/attempt/head, original producer run/artifact identity/digest, checker-v4
SHA, producer-v5 SHA, independent-result SHA, all six receipt SHA values,
elapsed/RSS data and false claim flags.  Upload success-only: result, six
receipts and workflow receipt.  Upload logs always.  Never upload a
mathematical success artifact after nonzero checker exit.

## Bounded checks and reply

Run safe YAML parse, source stat/hash checks, fire-gate/static DAG checks and
checker-v4 `py_compile/--selftest` only.  No real parent download/replay.
Report exact workflow bytes/LF/final-LF/SHA and:

```text
REAL_CHECKER_ONLY_GHA=NOT_RUN
P1_PRODUCER_SIX_PHASES=ACTUAL_SUCCESS
P1_SEMANTICS_CROSS_CHECKED=NO
A0/COMMON/COFINAL/FAKE/IHARA=NOT_DECLARED
verified=false
```

