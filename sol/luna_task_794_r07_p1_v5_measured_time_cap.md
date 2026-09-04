# Luna Task 794 — canonical P1 v5 measured time-cap release

Role: Luna implementation support. Process every numbered section in order.
Do not run production, GHA, network, git, or edit any existing file. Write
only the two versioned outputs named below:

- `.github/workflows/d972-r07-canonical-p1-dag-degree2-lift-v5.yml`
- `sol/luna_reply_794_r07_p1_v5_measured_time_cap.md`

## 1. Read the exact authority

Read in full:

- `sol/sol_reply_792_root_r07_p1_v4_resource_result.md`
- `.github/workflows/d972-r07-canonical-p1-dag-degree2-lift-v4.yml`
- `sol/sol_reply_784_audit_r07_canonical_p1_v7_v4.md`

Actual v4 reached cursor 6400/8059 in 36.40 producer minutes with stable
4.849 GiB RSS. The measured late rate projects recurrence EOF at 48.58
minutes. The arithmetic and all accepted pins are frozen.

## 2. Make only the measured workflow repair

Create v5 from exact v4 with no producer, checker, source, schema, command,
selftest, validation, artifact-content, arithmetic, input, or pin change.
The only semantic resource changes are:

- workflow name and push-fire tag become v5;
- job `timeout-minutes` becomes 75;
- `D972_LIFT_SECONDS` becomes `3540`;
- the external GNU `timeout` becomes `60m`;
- launch-step display text becomes canonical v5;
- success/log artifact names use task794 and v5.

Keep schema `d972.r07.canonical-p1-dag-degree2-lift.launch.v6` and candidate
schema `d972.r07.canonical-p1-dag-degree2-lift.v6`: no data-format change has
occurred. Do not add checkpoint/resume, parallelism, profiling, extra replay,
extra SELFTEST, or any other repair.

## 3. Bounded checks only

Outside the repo, compare v4 and v5 structurally after normalizing precisely
the listed resource/name fields. Require no other diff. Check YAML text has a
final LF and report exact bytes/SHA/LF. If a local YAML parser is already
available it may be used; do not install anything and do not run the actual
workflow.

## 4. Reply boundary

Report the exact normalized diff and identities. State clearly that v5 is a
release candidate only and root remains the sole git/GHA broker. End with

`READY_FOR_ROOT_RELEASE_REVIEW=yes`
