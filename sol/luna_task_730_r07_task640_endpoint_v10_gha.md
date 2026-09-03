# Luna Task730 - Task640 endpoint-minimal v10 GHA wrapper

## Scope

Create one inert, versioned workflow from the accepted v9 wrapper and the
Task723-accepted v4 pair. Do not edit Python sources, run GHA, or perform git.
Root will inspect, arm, commit, push and dispatch immediately.

Read in full:

- `.github/workflows/d972-r07-a0-fresh-precision2-endpoint-v9.yml`
- `sol/proof_r07_task640_endpoint_minimal_runtime_v484.md`
- `sol/luna_reply_717_r07_task640_endpoint_minimal_runtime_v4.md`
- `sol/sol_reply_723_audit_r07_task717_endpoint_minimal_v4.md`
- `search/d972_r07_a0_fresh_precision2_endpoint_signature_v4.py`
- `search/check_d972_r07_a0_fresh_precision2_endpoint_signature_v4.py`

Create only:

- `.github/workflows/d972-r07-a0-fresh-precision2-endpoint-v10.yml`
- `sol/luna_reply_730_r07_task640_endpoint_v10_gha.md`

## Exact wrapper

Preserve v9's exact accepted Task625/Task554/Task595 run, job, artifact and
action pins, resource environment, Python/numpy version, download paths and
success-only upload discipline. Change only what follows:

- workflow/version/artifact labels v9 -> v10;
- producer path/hash to v4 and
  `faa63bfd57629855101038c694130277b9c9d47120105341f9e89d12c8c3df08`;
- checker path/hash to v4 and
  `581f9a5a9aa65ae298bf6d6f785ed1063ddfb0caf8a0c06e15f30ec2e713fd6f`;
- Task717 reply SHA to
  `1e0d117a6fb7accc6b568e92bf6e74f9d1c34e8c133ab9e9ca30ff2912295cfd`;
- authenticate v484 SHA
  `25e292c8d996000c5dd442619f9afa269d83193ce5f58e4f3536c55b61f77492`
  and Task723 reply SHA
  `d6dfa91766e2d2eb52dd5fd1bfb5267a89d2277395aff401c3dfdcb60a55b6b4`;
- require checker marker
  `R07_FRESH_PRECISION2_ENDPOINT_SIGNATURE_V4_CHECKER_PASS`.

Keep the actual producer and checker command outer bounds at 45 minutes each,
the job bound at 120 minutes, `TASK640_SECONDS=9600` for the fresh step,
7-GiB internal RSS and 8-GiB virtual-memory guard. Keep unbuffered progress
visible through tee and always upload logs.

### Remove the redundant 11m51 parent replay

Do not rerun `search/check_d972_r07_a0_grade1_selected_slp_v2.py` in v10.
Task723 explicitly permits omission because both accepted v4 programs
independently enforce the fixed Task625 manifest, every exact payload file
size/SHA, canonical roots and leaf reconstruction, exact checker verdict SHA,
and byte equality of `task625-replayed-verdict.json` with that verdict.

Retain the v9 GitHub API authentication of the exact Task625 run/job/artifact
and download the same immutable artifact. Do not add copies to its payload;
the artifact already contains both exact verdict files. Artifact identity
without the in-program v4 gates would be insufficient, so keep the v4 source
pins and Task723 pin load-bearing.

Keep the workflow inert with `if: ${{ false }}`. Root will replace only that
guard after static inspection. Run a YAML parse/static shell review only; no
dispatch. Reply with exact files/bytes/LF/final-LF/SHA-256, exact v9/v10 diff,
step list, expected 11m51 saving, `WORKFLOW_INERT=true`, and `verified=false`.
