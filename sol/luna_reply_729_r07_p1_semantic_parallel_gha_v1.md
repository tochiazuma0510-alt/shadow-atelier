# Luna Task729 - P1 semantic parallel GHA wrapper v1

```text
RESULT=COMPLETE
WORKFLOW_INERT=true
GHA_DISPATCHED=false
verified=false
```

Created the commissioned inert workflow only.  Neither audited Python source
was edited, no Task554 artifact was downloaded locally, and no GHA or git
operation was performed.

## Exact frozen output

| path | bytes | LF | final LF | SHA-256 |
|---|---:|---:|:---:|---|
| `.github/workflows/d972-r07-p1-componentwise-semantic-v1.yml` | `36336` | `788` | yes | `9a70a3122e187972b4c3cd50aa7ec3e48e4630ce4f1013aa0dca3adfdf758b60` |

The reply's own exact receipt is reported externally after sealing to avoid a
self-referential digest.

## Pins and authenticated parents

The workflow pins Python `3.13`, NumPy `2.5.1`, producer-v4
`ff50d0ad50e080a15075bb52365987d9e389bf59e5e39666002b710947287a17`,
and checker-v2
`8636440c5e51d71a1f06d20d89a3d60c588453e741b17fbbd61735c76a9d3e88`.
Preflight authenticates their bytes/LF/final-LF receipts and also authenticates:

| audit reply | bytes | LF | final LF | SHA-256 |
|---|---:|---:|:---:|---|
| `sol/sol_reply_721_audit_r07_task720_p1_semantic_v4.md` | `5391` | `120` | yes | `922a7da011820f0ff2def256613767f565cfc987d8563265df5a15b2df9f9aa6` |
| `sol/sol_reply_726_audit_r07_task724_p1_checker_v2.md` | `12288` | `268` | yes | `c7a917e6dd93e34d2ba9ecf9a2cb6bb22b0e30d7f7533566554471cb5d3690eb` |

All actions use the already accepted literal SHAs:

| action | SHA |
|---|---|
| `actions/checkout` | `11d5960a326750d5838078e36cf38b85af677262` |
| `actions/setup-python` | `8d9ed9ac5c53483de85588cdf95a591a75ab9f55` |
| `actions/download-artifact` | `d3f86a106a0bac45b974a628896c90dbdf5c8093` |
| `actions/upload-artifact` | `65462800fd760344b1a7b4382951275a0abb4808` |

Preflight checks source run `33677346616`, attempt `1`, head
`22c6dddb43d107c05e65f53ad898823ae8ebe276`, then checks each immutable
artifact object for id, name, byte size, digest, unexpired state, run and head:

| phase | id | exact name | bytes | digest |
|---|---:|---|---:|---|
| prepare | `9865061266` | `task554-grade1-v3-prepare-33677346616-1` | `204360988` | `sha256:da8bfec6a03cac65de40ba8c4f79cde687fd2629edb3c3965fd972ecf96cc2f4` |
| block 0 | `9865238399` | `task554-grade1-v3-state-block-0-33677346616-1` | `81729645` | `sha256:2a8e63a4270bf4052c7fd8763d7828fc17dd6b94c88854bacde1e94082cd5838` |
| block 1 | `9865242284` | `task554-grade1-v3-state-block-1-33677346616-1` | `82259824` | `sha256:849321b79f0e3ea3c9a3f9c9dad43de2b3aaa571163456abc702476e322714fb` |
| block 2 | `9865193269` | `task554-grade1-v3-state-block-2-33677346616-1` | `82200189` | `sha256:d2cdf8245d58a384bebfd516135e07930fe26c21c2c1cab130dfa6c3c7f2854d` |
| block 3 | `9865239848` | `task554-grade1-v3-state-block-3-33677346616-1` | `82266526` | `sha256:87547101ede2fb48619a069de958c08cbb3cb0ee6c0990090234005aacd05b92` |

## Inert DAG and exact commands

Every one of the five job definitions has the literal job guard
`if: ${{ false }}`.  The dependency graph is:

```text
preflight -> prepare -> block[0,1,2,3]
prepare + block[0,1,2,3] -> join -> independent-check
```

- `preflight` pins/authenticates inputs, installs NumPy, compiles both sources,
  and runs producer/checker selftests under `5m`/`10m` command caps.
- `prepare` downloads only the prepare root and invokes producer-v4 with
  `--prepare-replay PREP_ROOT`.
- the four parallel `block` matrix children each download the prepare root and
  exactly their indexed block, then invoke
  `--block-replay PREP_ROOT BLOCK_ROOT --index i`.
- `join` downloads the five current-run phase artifacts in order and invokes
  `--join-receipts PREP B0 B1 B2 B3`.
- `independent-check` downloads the resulting six receipts and the exact five
  raw roots, then invokes checker-v2 compact mode with exactly twelve values:
  five roots, prepare plus ordered block receipts 0--3, join receipt, output.

Every producer phase tees complete stdout, requires its final LF, extracts
only `tail -n 1`, and accepts that line only after canonical-JSON and expected
schema/phase or terminal checks.  Prepare and blocks retain
`independent_checker=false`; join alone exposes the producer terminal
`TASK554_P1_COMPONENTWISE_SEMANTICS_REPLAYED`.  No earlier progress line can
be uploaded as a receipt.

Checker stdout must end in its immutable audited source marker
`R07_GRADE2_P1_COMPONENTWISE_INDEPENDENT_CHECKER_V1_PASS`.  The atomic result
is then canonicalized, checked for the independent terminal and all six raw
producer-receipt digests, and only then emits the commissioned workflow marker
`TASK554_P1_COMPONENTWISE_SEMANTICS_V2_CHECKER_PASS`.  The success upload is
additionally gated on that marker step's `passed=true` output.

## Bounds and artifacts

Job wall bounds are `20m` preflight, `360m` prepare, `360m` per block, `30m`
join and `360m` independent-check.  Heavy commands have `345m` external caps;
join has `20m`.  Producer/checker internal caps are each `19800` seconds and
`8589934592` RSS bytes; calculation shells also set `ulimit -v 12000000`.
Timeout/kill statuses create an `UNKNOWN_RESOURCE` log, fail the job, and
cannot reach a success artifact.

Current-run mathematical artifact names are:

```text
task729-p1-semantic-prepare-<run>-<attempt>
task729-p1-semantic-block-{0,1,2,3}-<run>-<attempt>
task729-p1-semantic-six-receipts-<run>-<attempt>
task729-p1-semantic-independent-success-<run>-<attempt>
```

The six-receipt artifact contains canonical prepare, ordered blocks 0--3 and
join receipts.  The final success artifact contains the checker result and
those exact six receipts, and nothing is uploaded there until both markers
and all result assertions pass.  Separate unique preflight/prepare/block/join/
checker log artifacts use `if: always()`.  Every upload uses retention `90`
days and compression level `0`.

## Static checks

```text
PyYAML safe_load: PASS
jobs=5; inert guards=5; DAG=PASS
matrix indices=[0,1,2,3]
pinned action references=33; unpinned action references=0
Task554 source metadata equality against structural workflow: PASS (23 fields)
producer phase CLI/static receipt extraction: PASS
checker compact positional count=12
audited-marker plus required-release-marker gate: PASS
embedded Python compile: PASS (5 snippets)
heredoc/static shell structure: PASS (5 heredocs; no CR or trailing-backslash space)
bash runtime/actionlint: NOT_RUN (not available locally)
workflow dispatch: NOT_RUN
```

No producer/checker receipt promotes precision two, A0, COMMON, compatible
lift, fake, Ihara or Lean verification.  The independent result alone may set
`independent_checker=true`; all downstream claims remain false.

```text
WORKFLOW_INERT=true
REAL_TASK554_REPLAY=NOT_RUN
INDEPENDENT_P1_RESULT=NOT_RUN
precision2=false
A0=false
COMMON=false
COMPATIBLE_LIFT=false
FAKE=false
IHARA=false
verified=false
```
