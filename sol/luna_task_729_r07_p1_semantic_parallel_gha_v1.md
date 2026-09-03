# Luna Task729 - P1 semantic parallel GHA wrapper v1

## Scope

Create one inert, versioned GitHub Actions workflow which runs the already
audited producer v4 and checker v2. Do not edit either Python source, run GHA,
or perform git. Root will inspect, arm, commit, push and dispatch.

Read in full:

- `sol/sol_reply_721_audit_r07_task720_p1_semantic_v4.md`
- `sol/sol_reply_726_audit_r07_task724_p1_checker_v2.md`
- `search/d972_r07_grade2_p1_componentwise_semantic_replay_v4.py`
- `crosscheck/check_d972_r07_grade2_p1_componentwise_semantics_v2.py`
- `.github/workflows/d972-r07-p1-structural-replay-v1.yml` for the exact
  Task554 source run/artifact ids, names, sizes and digests.

Create only:

- `.github/workflows/d972-r07-p1-componentwise-semantic-v1.yml`
- `sol/luna_reply_729_r07_p1_semantic_parallel_gha_v1.md`

## Workflow

Use pinned action SHAs and Python 3.13. Pin producer exactly to
`ff50d0ad50e080a15075bb52365987d9e389bf59e5e39666002b710947287a17`
and checker exactly to
`8636440c5e51d71a1f06d20d89a3d60c588453e741b17fbbd61735c76a9d3e88`.
Authenticate the exact five Task554 artifacts from run `33677346616/1` using
the immutable ids/names/sizes/digests/head already recorded in the structural
workflow. Authenticate Task721/Task726 reply bytes too.

Keep every calculation job inert with `if: ${{ false }}`. Root alone will arm
it after inspection.

Use this DAG:

```text
preflight
  -> prepare
  -> block matrix 0,1,2,3 (four parallel jobs)
prepare + all blocks -> join
join -> independent-check
```

- `preflight`: source/artifact authentication, install pinned numpy, py_compile,
  producer/checker bounded selftests.
- `prepare`: download only prepare root; run producer `--prepare-replay`.
- each block: download prepare plus its exact indexed block; run producer
  `--block-replay PREP BLOCK --index i`.
- `join`: download the five current-run phase receipt artifacts; run producer
  `--join-receipts PREP B0 B1 B2 B3`; upload a six-receipt artifact containing
  prepare, ordered blocks 0--3 and join.
- `independent-check`: download the six receipts and all five raw Task554 roots;
  invoke checker-v2 compact mode with exactly its 12 positional values (five
  roots, five phase receipts, join receipt, output), require marker
  `TASK554_P1_COMPONENTWISE_SEMANTICS_V2_CHECKER_PASS`, and upload success
  result plus six receipts only after that marker.

The imported grade1-v4 helpers print progress to stdout. For every producer
phase, tee complete stdout to a log and take exactly the final line as the
canonical phase/join receipt; parse it, require final LF/canonical JSON and the
expected schema/phase/terminal before upload. Never treat earlier progress
lines as a receipt.

Use unique current-run artifact names, 90-day retention, compression level 0
for large/log artifacts, success-only mathematical artifacts and always-upload
logs. Set explicit job/command wall bounds, `TASK709_SECONDS`, checker seconds,
RSS bounds and `ulimit -v` without turning a cap into a negative result. A cap
or missing output fails/UNKNOWN and must not upload the final success artifact.

Do not put real artifact roots in the repository. Do not add a producer-only
claim beyond `TASK554_P1_COMPONENTWISE_SEMANTICS_REPLAYED`; only the final
checker result may carry the independent marker, and all downstream claims
remain false.

Run only a YAML parse/static shell review if available; no workflow dispatch.
Reply with exact files/bytes/LF/final-LF/SHA-256, job DAG, pins, commands,
timeouts/artifact names, static checks, `WORKFLOW_INERT=true`, and
`verified=false`.
