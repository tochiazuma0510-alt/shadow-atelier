# Luna Task747 -- P1 semantic producer-v5/checker-v3 GHA rerun

```text
RESULT=COMPLETE
REAL_GHA_RUN=NOT_RUN
verified=false
```

Created only the commissioned v2 workflow and this reply.  The workflow
retains the Task729 prepare -> four parallel block jobs -> join -> independent
checker DAG, all five Task554 artifact IDs/digests, ranks, time/RSS caps,
canonical receipt gates, six positional checker receipt arguments, and false
claim flags.  Producer v5 and checker v3 are pinned at the requested bytes,
LF counts, and SHA-256 values.  The actual checker marker remains
`R07_GRADE2_P1_COMPONENTWISE_INDEPENDENT_CHECKER_V1_PASS`; no arithmetic or
schema marker was invented.  The workflow-only release label is
`TASK554_P1_COMPONENTWISE_SEMANTICS_V3_CHECKER_PASS` and is explicitly marked
non-authoritative.

The workflow has only the existing branch/path push trigger, with
`[fire-r07-p1-semantic-v2]` required on every job.  Internal task729 temporary
and artifact labels remain unchanged so the dependency DAG is stable.  The
v489 proof, Task740 reply, and Task743 audit are authenticated by exact bytes,
LF count, final LF, and SHA-256; the two exact audit tokens are required.
No prepare, block, join, independent check, real replay, Git, push, or GHA
dispatch was performed.

## Exact receipts

| path | bytes | LF | final LF | SHA-256 |
|---|---:|---:|:---:|---|
| `.github/workflows/d972-r07-p1-componentwise-semantic-v2.yml` | `37797` | `810` | yes | `3093b73908a04a57abbd57e925eea9fa59f1109f7ab984f760c160a6f127661c` |
| `search/d972_r07_grade2_p1_componentwise_semantic_replay_v5.py` | `41619` | `382` | yes | `dc5931c3fd3ad5d1a947346599824b02ad1d7b5f699361c05f1f051076dcbdcf` |
| `crosscheck/check_d972_r07_grade2_p1_componentwise_semantics_v3.py` | `130683` | `2689` | yes | `3cfdbe0485711b9b4a08db2d664ded7719a126e3a499724d33cd122a101e774e` |
| `sol/proof_r07_p1_equality_literal_lf_repair_v489.md` | `2771` | `69` | yes | `14e4d33967cea1a26d1cb41c11ab125abad2cc9d5455e3c85e0377987832c789` |
| `sol/luna_reply_740_r07_p1_equality_literal_lf_v5.md` | `3340` | `75` | yes | `512d480ce007a2573eaf6ec8fa9fbbb3623a741d08000e33edef16f23c0dfe1a` |
| `sol/sol_reply_743_audit_r07_p1_equality_lf_v5.md` | `12090` | `228` | yes | `a3b4a3719c6464b795a2e0a935d1366cd727674aad39609f193af271a422377f` |

The reply's own digest is supplied post-seal rather than embedded, avoiding a
self-referential receipt.

## Bounded checks

```text
python -B search/d972_r07_grade2_p1_componentwise_semantic_replay_v5.py --selftest
exit 0; status=PASS; fixture_accept=2; rejections=35; actual_replay=DEFERRED_TO_GHA

python -B crosscheck/check_d972_r07_grade2_p1_componentwise_semantics_v3.py --selftest
exit 0; status=PASS; fixture_accept=6; rejections=41; actual_five_artifact_check=DEFERRED_TO_GHA
```

YAML parsing passed; all five jobs carry the v2 fire tag, and stale v1,
producer-v4, checker-v2, and workflow-dispatch strings are absent.  No
artifact or replay receipt was produced.
