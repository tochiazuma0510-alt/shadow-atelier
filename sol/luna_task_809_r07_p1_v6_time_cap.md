# Luna Task809 — canonical P1 degree-two v6: measured time-cap repair only

Role: minimal workflow repair.  Process every numbered section first to last.
Do not change Python code, run GHA, commit, push, add a checkpoint framework,
or alter mathematics.  Create only the new workflow and designated reply.

## 1. Read the exact evidence

Read in full:

- `.github/workflows/d972-r07-canonical-p1-dag-degree2-lift-v5.yml`
- `sol/sol_reply_796_root_r07_p1_v5_launch.md`
- `C:/Users/81905/Desktop/shadow-atelier-artifacts/gha/run33833873366-attempt1-task794-logs/build.log`
- `C:/Users/81905/Desktop/shadow-atelier-artifacts/gha/run33833873366-attempt1-task794-logs/build-status.txt`
- `C:/Users/81905/Desktop/shadow-atelier-artifacts/gha/run33833873366-attempt1-task794-logs/unknown-resource.json`

Run/attempt `33833873366/1`, job `100902284260`, head
`011780dea7ced10f36b65f428616c453fe87cf8a`, stopped with exit 124 at the
inner shell `60m` limit.  Its last complete checkpoint is cursor 7,040 of
8,059 (87.3558%), elapsed 3,537.254897481 seconds, durable bytes 538,893,700
and RSS 5,223,956,480 bytes.  This is not a memory stop and no mathematical
terminal was emitted.

## 2. Create only

- `.github/workflows/d972-r07-canonical-p1-dag-degree2-lift-v6.yml`
- `sol/luna_reply_809_r07_p1_v6_time_cap.md`

V5 and every executable remain byte-identical.

## 3. Change only the measured caps and version labels

Clone v5 faithfully, then make these bounded changes:

- workflow/job outer timeout: 100 minutes;
- `D972_LIFT_SECONDS`: `5100`;
- inner GNU `timeout`: `85m` with the existing 30-second kill-after;
- workflow name, dispatch fire tag, launch label and candidate/log artifact
  names advance honestly from v5/Task794 to v6/Task809.

Keep `D972_LIFT_MAX_RSS=7516192768`, `ulimit -v 8388608`, one serial producer,
all exact source/semantic/checker pins, NumPy/thread settings, terminal manifest
checks, success-only candidate upload, always-upload logs, and all false claim
flags unchanged.  Do not parallelize dependent rows, add a production test,
or change the expected 8,059 rows / 292,444,992 cache bytes.

The measured last 384-row interval was about 178.71 seconds; simple local
projection puts the remaining 1,019 rows near 474 seconds, while the complete
post-2,048 average gives about 656 seconds.  The new cap therefore leaves a
bounded margin without changing the computation.

## 4. Static checks and reply

Perform only YAML/static pin checks.  Confirm no executable hash/path or
arithmetic command changed and that the new three caps occur exactly once in
their intended fields.  Report workflow bytes/LF/CR/BOM/SHA-256, the exact
v5 terminal evidence above, and `READY_FOR_ROOT_DISPATCH` or
`NOT_READY:<reason>`.

State that canonical P1 acceptance, grade-two MEMBER/NONMEMBER, A0, COMMON,
compatible lift, fake and Ihara are not claimed; `verified=false`.
