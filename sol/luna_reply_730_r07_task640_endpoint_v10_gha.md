# Luna reply 730 - Task640 endpoint-minimal v10 GHA wrapper

## Result

Created only the inert workflow and this reply. No Python source was edited;
no real parent, 59,049-entry build, GHA dispatch, or git operation was run.

`WORKFLOW_INERT=true`

`verified=false`

`REAL_TASK640_RUN=DEFERRED_TO_GHA`

`FRESH_RHO2=NOT_PRODUCED`

## Frozen receipts

| path | bytes | LF | final LF | SHA-256 |
|---|---:|---:|---|---|
| `.github/workflows/d972-r07-a0-fresh-precision2-endpoint-v10.yml` | 10,580 | 170 | yes | `464fbea95361e68ce244f0bf84c05a387dae4871d99e0bac96136787cd400c24` |
| `sol/luna_reply_730_r07_task640_endpoint_v10_gha.md` | 7,413 | 129 | yes | parent handoff (self-SHA) |
| v9 workflow baseline | 10,214 | 162 | yes | `732bd5d9b4cc9f2be145ff8a10081d13f9c58e3a4da10b6ef15ea903b04c8088` |
| `search/d972_r07_a0_fresh_precision2_endpoint_signature_v4.py` | 43,758 | 670 | yes | `faa63bfd57629855101038c694130277b9c9d47120105341f9e89d12c8c3df08` |
| `search/check_d972_r07_a0_fresh_precision2_endpoint_signature_v4.py` | 93,236 | 1,592 | yes | `581f9a5a9aa65ae298bf6d6f785ed1063ddfb0caf8a0c06e15f30ec2e713fd6f` |
| `sol/proof_r07_task640_endpoint_minimal_runtime_v484.md` | 6,571 | 159 | yes | `25e292c8d996000c5dd442619f9afa269d83193ce5f58e4f3536c55b61f77492` |
| `sol/luna_reply_717_r07_task640_endpoint_minimal_runtime_v4.md` | 3,631 | 85 | yes | `1e0d117a6fb7accc6b568e92bf6e74f9d1c34e8c133ab9e9ca30ff2912295cfd` |
| `sol/sol_reply_723_audit_r07_task717_endpoint_minimal_v4.md` | 11,382 | 215 | yes | `d6dfa91766e2d2eb52dd5fd1bfb5267a89d2277395aff401c3dfdcb60a55b6b4` |

The reply's own post-freeze SHA is supplied in the parent handoff because
embedding a self-SHA would change the bytes.

## Exact v9 -> v10 diff

The raw comparison has no changes outside the entries below:

```diff
- name: d972-r07-a0-fresh-precision2-endpoint-v9
+ name: d972-r07-a0-fresh-precision2-endpoint-v10
- search/d972_r07_a0_fresh_precision2_endpoint_signature_v3.py
+ search/d972_r07_a0_fresh_precision2_endpoint_signature_v4.py
- search/check_d972_r07_a0_fresh_precision2_endpoint_signature_v3.py
+ search/check_d972_r07_a0_fresh_precision2_endpoint_signature_v4.py
- sol/luna_reply_640_r07_fresh_precision2_endpoint_signature_v3.md
+ sol/luna_reply_717_r07_task640_endpoint_minimal_runtime_v4.md
- .github/workflows/d972-r07-a0-fresh-precision2-endpoint-v9.yml
+ .github/workflows/d972-r07-a0-fresh-precision2-endpoint-v10.yml
- PRODUCER_SHA256: "8719929bfd6d134320da8c6fc1a8df527f458c1523f8edb0330b539649097206"
+ PRODUCER_SHA256: "faa63bfd57629855101038c694130277b9c9d47120105341f9e89d12c8c3df08"
- CHECKER_SHA256: "889b7c7753e53e9c73c5edd575443446b0e3051794d6f20356809244c57cbd32"
+ CHECKER_SHA256: "581f9a5a9aa65ae298bf6d6f785ed1063ddfb0caf8a0c06e15f30ec2e713fd6f"
- REPLY_SHA256: "a187b207f4cbf97c0b20fe28c8edd33a39f60cbdf34909a5cfba56000dd4287b"
+ REPLY_SHA256: "1e0d117a6fb7accc6b568e92bf6e74f9d1c34e8c133ab9e9ca30ff2912295cfd"
+ V484_SHA256: 25e292c8d996000c5dd442619f9afa269d83193ce5f58e4f3536c55b61f77492
+ TASK723_REPLY_SHA256: d6dfa91766e2d2eb52dd5fd1bfb5267a89d2277395aff401c3dfdcb60a55b6b4
- if: ${{ github.event_name == 'workflow_dispatch' || contains(github.event.head_commit.message, '[fire-fresh-precision2-endpoint-v9]') }}
+ if: ${{ false }}
- Authenticate v9 and pinned arithmetic source
+ Authenticate v10 and pinned arithmetic source
- v3 producer/checker paths in source authentication, fixtures, and commands
+ v4 producer/checker paths in source authentication, fixtures, and commands
+ source authentication of the v484 proof and Task723 audit reply
- Rerun exact Task625 checker and compare uploaded verdict
+ Stage authenticated Task625 verdict into payload
+ verify top-level verdict is 1,120 bytes, SHA-256 a650aa8d5d78f52145fff5ba7769ad2036cfd16e90e3caaf367b4517e07d2740, and has the accepted marker
+ copy that exact byte stream to payload/task625-verdict.json and payload/task625-replayed-verdict.json, then cmp all three
- R07_FRESH_PRECISION2_ENDPOINT_SIGNATURE_V3_CHECKER_PASS
+ R07_FRESH_PRECISION2_ENDPOINT_SIGNATURE_V4_CHECKER_PASS
- task640-fresh-rho2-v9-${{ github.run_id }}-${{ github.run_attempt }}
+ task640-fresh-rho2-v10-${{ github.run_id }}-${{ github.run_attempt }}
- task640-fresh-rho2-v9-logs-${{ github.run_id }}-${{ github.run_attempt }}
+ task640-fresh-rho2-v10-logs-${{ github.run_id }}-${{ github.run_attempt }}
```

All accepted Task625/Task554/Task595 run, attempt, job, head, workflow,
artifact, download, and action pins remain byte-identical to v9. The resource
environment is unchanged: global `TASK640_SECONDS=5400`, fresh-step
`TASK640_SECONDS=9600`, `TASK640_MAX_RSS=7516192768`, and
`ulimit -v 8388608`. Python is 3.13, numpy is 2.5.1, both production
commands retain `timeout ... 45m`, the job remains 120 minutes, progress is
unbuffered through `tee`, residual upload is success-only, and logs upload on
`always()`.

## Steps

1. Checkout exact event SHA.
2. Setup Python 3.13.
3. Authenticate v10, the v4 pair, Task717 reply, v484 proof, Task723 reply,
   and the unchanged arithmetic/source pins.
4. Run bounded serial fixtures (numpy 2.5.1, v4 compile/selftest commands).
5. Authenticate the exact accepted Task625 run/job/artifact through GitHub API.
6. Download the exact accepted Task625 parent artifact.
7. Download exact Task554 source state.
8. Download exact Task595 MEMBER candidate.
9. Stage and authenticate the downloaded top-level Task625 verdict, then copy
   it byte-for-byte to the two v4-required payload verdict names and `cmp`.
10. Produce and independently check fresh rho2 with the two bounded 45-minute
   commands and the v4 checker marker gate.
11. Upload residual only after `success()`.
12. Upload logs on `always()`.

## Task625 replay gate

The redundant parent checker replay is omitted, saving the expected `11m51s`.
The downloaded artifact's top-level `task625-verdict.json` is first required
to be exactly 1,120 bytes, SHA-256
`a650aa8d5d78f52145fff5ba7769ad2036cfd16e90e3caaf367b4517e07d2740`, and to
contain `R07_GRADE1_SELECTED_SLP_V2_CHECKER_PASS`; it is then copied unchanged
to both payload names required by v4 and all three copies are compared. This
staging is not a checker replay. With exact GitHub run/attempt/artifact
identity retained, both v4 programs independently reauthenticate the fixed
Task625 manifest, every payload file name/size/SHA, canonical roots and leaf
reconstruction, the exact checker verdict SHA and marker, and byte equality of
`task625-replayed-verdict.json` with that verdict. The v4 source pins and
Task723 audit pin remain load-bearing. If either side blindly trusted a peer
verdict, or if only artifact identity were checked, the Task625 checker rerun
would be mandatory.

## Static review

YAML parse passed with `yaml.safe_load`; the document has one
`fresh-endpoint` job and 12 steps. Static shell review passed: five run blocks
have `set -euo pipefail`; the two producer/checker commands each have a 45m
outer timeout and `tee`; the staging block checks the exact 1,120-byte
verdict/SHA/marker and performs only the two required byte copies plus `cmp`;
no Task625 checker replay command remains; the v4 marker is required; the job
guard is exactly `${{ false }}`; and residual/log upload conditions are
`success()`/`always()`.
No workflow execution, GHA dispatch, git operation, producer selftest,
checker selftest, parent build, or actual 59,049-entry construction was run.
