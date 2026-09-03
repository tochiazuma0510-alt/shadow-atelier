# Luna Task751 -- P1 checker-only GHA v1

```text
RESULT=COMPLETE
REAL_CHECKER_ONLY_GHA=NOT_RUN
P1_PRODUCER_SIX_PHASES=ACTUAL_SUCCESS
P1_SEMANTICS_CROSS_CHECKED=NO
A0/COMMON/COFINAL/FAKE/IHARA=NOT_DECLARED
verified=false
```

Created only the designated checker-only workflow and this reply:

```text
.github/workflows/d972-r07-p1-semantic-checker-only-v1.yml
sol/luna_reply_751_r07_p1_checker_only_gha_v1.md
```

The workflow is push-only on `sol/r07-explicit-lift-20260825`, watches only
its own path, has no `workflow_dispatch`, and every job requires the exact
`[fire-r07-p1-checker-only-v1]` commit-message gate. Checkout, setup-python,
download-artifact, and upload-artifact are pinned to the v2 SHAs; NumPy is
pinned to `2.5.1`.

## Immutable inputs and authentication

The workflow does not regenerate producer data.  It authenticates the exact
producer run/attempt/head and artifact metadata, downloads the artifact from
that run, and requires exactly the six canonical prepare/block-0--3/join
receipts before checker-v4 is called.

```text
producer run/attempt 33814881435/1
producer head        15778e83c52941040ef9d4289ab76d897ee30ebc
producer artifact    9916479231
producer name        task729-p1-semantic-six-receipts-33814881435-1
producer bytes       8412
producer digest      sha256:91281261a272e6ff48104a579a86e9cb300fc1543eaad1321b609e6d83564245
producer-v5 SHA      dc5931c3fd3ad5d1a947346599824b02ad1d7b5f699361c05f1f051076dcbdcf
```

The five Task554 parents retain the v2 run/layout and are authenticated by
id, name, byte size, digest, non-expired state, source run, and source head:

| phase | artifact id | archive bytes | digest |
|---|---:|---:|---|
| prepare | 9865061266 | 204360988 | `sha256:da8bfec6a03cac65de40ba8c4f79cde687fd2629edb3c3965fd972ecf96cc2f4` |
| block-0 | 9865238399 | 81729645 | `sha256:2a8e63a4270bf4052c7fd8763d7828fc17dd6b94c88854bacde1e94082cd5838` |
| block-1 | 9865242284 | 82259824 | `sha256:849321b79f0e3ea3c9a3f9c9dad43de2b3aaa571163456abc702476e322714fb` |
| block-2 | 9865193269 | 82200189 | `sha256:d2cdf8245d58a384bebfd516135e07930fe26c21c2c1cab130dfa6c3c7f2854d` |
| block-3 | 9865239848 | 82266526 | `sha256:87547101ede2fb48619a069de958c08cbb3cb0ee6c0990090234005aacd05b92` |

Source run/attempt/head is `33677346616/1/22c6dddb43d107c05e65f53ad898823ae8ebe276`.
The workflow authenticates exact bytes/LF/final-LF for producer-v5,
checker-v4, proof-v493, the Task749 reply, and the Task750 audit, and requires
both Task750 tokens:

```text
VERDICT=PASS_P1_CHECKER_STATE_HEAD_V4_SAFE_FOR_GHA
SAFE_TO_DISPATCH_CHECKER_ONLY_GHA=yes
```

## Checker-only contract

Checker-v4 selftest and compilation run before any large input download.  The
only arithmetic invocation is checker-v4 `--check` with the exact five v2
parent roots followed by the six positional receipt paths and output path.
It preserves the 345-minute process timeout, 360-minute job timeout,
`ulimit -v 12000000`, single BLAS threads, `/usr/bin/time -v` elapsed/RSS
logging, and timeout-to-`UNKNOWN_RESOURCE` routing.  It requires the existing
audited marker
`R07_GRADE2_P1_COMPONENTWISE_INDEPENDENT_CHECKER_V1_PASS`.

The post-check gate requires the canonical independent result, exact source
ancestry and counts, producer-v5 SHA, all six raw receipt SHA-256 values,
`independent_checker=true`, and false downstream flags.  The workflow receipt
binds current run/attempt/head, producer run/artifact identity/digest,
checker-v4 and producer-v5 SHAs, independent-result SHA, all receipt SHAs,
elapsed/RSS, and the eight downstream claim flags, all false.  Only successful
checks upload result/receipts; logs upload always, and a nonzero checker never
uploads a mathematical success artifact.

## Exact source and workflow receipt

| path | bytes | LF | final LF | SHA-256 |
|---|---:|---:|:---:|---|
| `.github/workflows/d972-r07-p1-semantic-checker-only-v1.yml` | 19927 | 391 | yes | `ed3195a7dfe57b8e0980675d5c9b67c2ddc6cb5b348089ef20a1088a806ee634` |
| `crosscheck/check_d972_r07_grade2_p1_componentwise_semantics_v4.py` | 132129 | 2719 | yes | `cc9a27e8ab447ecd6e4fbebbd1240195e442d6c5eb14241a5f9d7c669154ee19` |
| `search/d972_r07_grade2_p1_componentwise_semantic_replay_v5.py` | 41619 | 382 | yes | `dc5931c3fd3ad5d1a947346599824b02ad1d7b5f699361c05f1f051076dcbdcf` |
| `sol/proof_r07_p1_checker_state_head_schema_repair_v493.md` | 2414 | 80 | yes | `2feb9f83135cc4af234dfc7110128b2636fb12bd82e920ce3bdab19b02fddf5b` |
| `sol/luna_reply_749_r07_p1_checker_state_head_v4.md` | 3340 | 71 | yes | `2d93e8e576633d5b8d5bfc9434c266266054c89ff0a808dec782493bb8b0a316` |
| `sol/sol_reply_750_audit_r07_p1_checker_state_head_v4.md` | 10046 | 216 | yes | `a4a738ac814a5470ee471416380c00a51f1cfef555e32d63c273404fb34ef517` |

The reply's own digest is supplied post-seal rather than embedded.

## Bounded checks

```text
safe YAML parse + fire/DAG/pin/static checks: PASS
python -B -m py_compile crosscheck/check_d972_r07_grade2_p1_componentwise_semantics_v4.py: exit 0
python -B crosscheck/check_d972_r07_grade2_p1_componentwise_semantics_v4.py --selftest: exit 0
fixture_accept=7
rejections=42
actual_five_artifact_check=DEFERRED_TO_GHA
status=PASS
verified=false
```

No real parent download, producer replay, checker `--check`, GHA, Git, push,
dispatch, or actual build was performed.
