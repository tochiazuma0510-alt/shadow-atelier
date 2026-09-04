# Luna Task902 -- live physical-state / separator workflow v1

You are Luna.  After and only after Sol(max) Task900 accepts the frozen
Task899 executables, implement the smallest GHA workflow that runs their
fresh ordinary path on the two exact accepted parents.  Read AGENTS.md,
Tasks871/899 and reply871, Task900, rho2 flat-stager v4/Task894, and physical
connection workflow v11/Tasks892/896/result901 completely.  Do not change any
Python executable, mathematics paper, ledger, or existing workflow.  Do not
use Git, credentials, GHA dispatch, or production artifacts locally.

Create only:

1. `.github/workflows/d972-r07-grade2-physical-state-separator-v1.yml`;
2. `sol/luna_reply_902_r07_physical_state_separator_workflow_v1.md`.

## Exact immutable inputs

Query through the GitHub API and fail closed on repository, completed-success
run/attempt/head, artifact id/name/archive bytes/digest/expiry, non-expiry and
repository ids for both:

- connection v11: run `33876776771/1`, head
  `b44ec9bd078ce0a6ca596a38cfea5012f4fee4d2`, artifact id `9939860701`,
  name
  `d972-r07-canonical-p1-physical-connection-v11-candidate-33876776771-1`,
  bytes `245546516`, digest
  `sha256:0c3753d7384a7850aadab41c9ec2755114475862a0b03fd806e875005a72995a`,
  expiry `2026-12-03T13:12:28Z`;
- rho2-v17: run `33839962829/1`, head
  `17a8439c766d92719d7ae7d35846ea444da598fa`, workflow
  `.github/workflows/d972-r07-a0-fresh-precision2-endpoint-v17.yml`, artifact
  id `9925190479`, name `task640-fresh-rho2-v17-33839962829-1`, bytes
  `6049643`, digest
  `sha256:01722bfda081e577195aa6ca9c0bba3425a50dcfd829eca6ac23e33cb5d79ca4`,
  expiry `2026-12-03T05:17:47Z`.

Authenticate the frozen sources by exact bytes/LF/SHA from reply871 and
Task894.  Current accepted executable identities are:

```text
search/d972_r07_grade2_physical_state_separator_v1.py
  bytes=75934 LF=1407 sha256=5f1267a7296a6f613f46a1d431c807da22239419362f32ea7c08b51fd7d6e13f
search/check_d972_r07_grade2_physical_state_separator_v1.py
  bytes=57325 LF=734 sha256=01df70e8c6be4bfdff4fbedc227488edce47b1e9c195466ea7658d36b63ee107
search/stage_d972_r07_targeted_grade2_rho2_v9_flat_v4.py
  bytes=29738 LF=659 sha256=ce84baea0bc18380af8a20e32eb8862f9adc20ad596c2012e127f8b7b8341a4b
```

## Exact workflow

Use `ubuntu-24.04`, Python 3.13, pinned `numpy==2.5.1`, unbuffered output and
`compression-level: 0`.  Download the connection candidate and rho2 artifact
by exact name and run id into fresh runner-temp roots.  Construct the exact
rho2 acquisition JSON from the API receipts, then run accepted flat-stager v4
to a fresh flat root.  Do not hand-copy or partially select rho2 payloads.

Construct one canonical ASCII launch for the state producer with
`fixture_only=false`, `resume=false`, the exact live-parent/final-artifact,
producer/checker/stager identities, and runner-temp paths.  Run compile,
producer selftest, checker selftest and the bounded benchmark once.  Then run:

```text
producer --run-launch <launch>
checker  --check-launch <launch>
```

The state/output roots must be fresh.  Do not expose live resume, use an old
checkpoint, run a generic nullspace/SAT solve, rebuild PB3/PB4 closures, or
invoke any previous A0 exhaustive scan.  Preserve logs and periodic progress;
the actual physical phase has only 1,354 offered rows and at most 915,981
physical reductions.  Use a proportional cap (recommended 30 minutes per
producer/checker and 75 minutes for the job); a timeout/resource exit is
UNKNOWN and must not become NONMEMBER.

Upload an unchecked state/log artifact under `always()`.  Upload the final
state + terminal + independent checker result only when both named producer
and checker steps succeed.  Artifact labels must say candidate, never
verified.  The workflow may be triggered only by `workflow_dispatch` or one
unique audited commit marker; no automatic ordinary push run.

Run local YAML/static checks and bounded executable checks only.  Report the
exact two new-file receipts, caps, step graph, output rosters, and the one
marker string root should use.  End with either

```text
R07_PHYSICAL_STATE_SEPARATOR_WORKFLOW_V1_READY_FOR_SOL_AUDIT
```

or the first honest blocker.  Do not claim an actual grade-two result before
the GHA producer, independent checker and final publication complete.
