# Sol(max) Task639: audit successful Task625 selected-SLP artifact

## 1. Exact scope

Read this mail completely.  Independently audit the successful production
artifact as a parent for the v478/Task630 precision-two consumer.  Do not edit
implementation, rerun the full computation, dispatch GHA, or perform git.
Write only `sol/sol_reply_639_audit_r07_task625_success_artifact.md`.

## 2. Immutable run and local artifact

```text
workflow/run/attempt/job:
d972-r07-a0-grade1-selected-slp-staged-v3 / 33734643746 / 1 / 100582244001
head: b401d724bbdbef8cf67e96def22fc51c014ab546
conclusion: success
main step: success
payload upload: success
log upload: success
```

GitHub artifacts:

```text
payload id 9885925239
name task625-grade1-selected-slp-staged-v3-33734643746-1
archive bytes 50,793,121
digest sha256:ac3121f3bc1a7e2a6c267f20352e953b7343f9085015dd74e4a67e4b90129a75

logs id 9885925893
name task625-grade1-selected-slp-staged-v3-logs-33734643746-1
archive bytes 3,770
digest sha256:7cd8678a48dc0036beb0d1f887e1680145be8d1987272f35c9cce57982f0b86e
```

Downloaded outside the repository at
`%TEMP%/shadow-atelier-task625-33734643746-1/`.  Audit the exact files there.

## 3. Required exact bindings

Authenticate at least:

```text
manifest.json       9,034 bytes
sha256 381f961fc808076c5c0adbc98e32c19742565087bffbcd5f99772533e05d5c22

task625-verdict.json 1,120 bytes
sha256 a650aa8d5d78f52145fff5ba7769ad2036cfd16e90e3caaf367b4517e07d2740

producer.log        6,921 bytes
sha256 bfb54eb7decf3cd712f8dc225d33b7e12c5dc13cbd9a186fbba5b9553b7d8bdf

checker.log         8,982 bytes
sha256 5ee903d35000a38e654973acb853fed41a78e698a9736847dad3d4d16db922e3
```

Recompute all fifteen manifest receipt sizes and hashes rather than trusting
this mail.  Confirm their sum 232,502,114 plus manifest 9,034 equals the
inclusive payload size 232,511,148.

## 4. Mathematical/computational acceptance checks

Decide each item:

1. exact Task554/Task595 parents, cursor 8,059, offers 2,014/6,398, ranks
   1,661/5,044, 3,317 ordered coefficients, basis and zero remainder;
2. producer completes every `G,L,B0..B3,D,O0..O3,leaves` stage and seals
   the canonical graph/leaf stream and payload;
3. totals are exactly 14,920 processed nodes, 46,629 expanded states,
   7,682,296 state-edge traversals, 2,605,954 cumulative insertions, 2,565
   exact paths, maximum path length 24, maximum live 25,267, and 19,393
   leaves;
4. checker independently reproduces the staged statistics and exact leaf
   bytes, then exhausts the complete standalone 8,059-object physical route;
5. checker verdict marker is
   `R07_GRADE1_SELECTED_SLP_V2_CHECKER_PASS` and binds manifest, roots,
   ancestry, leaves, staged theorem/statistics, basis, prepare and remainder;
6. roots are ordered `C_T` (3,317 children), `C_<1` (2,622 stored terms),
   and `C_1=Compose(C_<1,C_T)`;
7. every manifest/root claim flag remains deliberately false/null:
   no direct occurrence replay, no next residual, no A0/COMMON/FAKE/IHARA,
   no Lean verification; and
8. resource receipts are within the declared bounds.  Record that a checker
   peak RSS around 5.51 GB is below 7 GiB rather than silently dropping it.

The checker verdict's own `cross_checked=false` is a self-promotion guard.
Decide whether the immutable producer plus independent checker plus this
external audit makes the artifact an **accepted selected-SLP parent** for
Task630; do not confuse that with a new grade numerator or A0.

## 5. Verdict

Return one of:

- `PASS_SELECTED_SLP_PARENT`: accepted input for a new versioned Task630/v478
  consumer implementation;
- `PASS_AFTER_REPAIR`: give one finite exact blocker;
- `FAIL`: the payload/checker equation is not trustworthy.

State the v220 mapping explicitly: A0 remains 0/1 actual and the first rung
remains 1/6 cross-checked; this success materializes the already decided
grade-one update and unlocks fresh rho2, but does not itself decide grade two,
full A0, a cofinal lift, fake, or Ihara.  `verified=false`.
