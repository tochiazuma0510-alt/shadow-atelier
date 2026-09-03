# Sol(max) Task638: audit Task625 staged-state-cap terminal and minimal rerun

Read this mail completely.  Perform a read-only adversarial audit of the
single GHA terminal from run/attempt/job
`33732940935/1 / 100576830812` at release commit
`c4ae5094800d4acb812eefb21820b9998afc3804`.

Read:

- the complete producer log at
  `%TEMP%/shadow-atelier-task625-33732940935-1/producer.log`, 4,534 bytes,
  SHA-256
  `e5c86f0750fe348d3c30e073ec94053c2753817a8097c8e5280c802ab2b68f37`;
- the exact v2 producer/checker/workflow and Task634 final PASS;
- `sol/luna_task_637_r07_task625_accumulated_cap_release_v3.md`.

Decide narrowly:

1. whether the terminal is exactly a cumulative insertion/work cap, rather
   than time, RSS, durable, interned-path, mathematical inconsistency, or
   live-state memory failure;
2. whether the completed stage telemetry demonstrates that the v475 staged
   schedule removed the former pathwise re-expansion problem;
3. whether a versioned workflow-only increase of
   `TASK625_ACCUMULATED_CAP` from 2,000,000 to 50,000,000 is a sound minimal
   rerun, with the unchanged 7-GiB RSS and 40/45/60-minute clocks remaining
   the real safety boundary;
4. whether either Python executable must change; and
5. which exact claims remain false/unknown after this failed run.

Do not demand a generalized cap framework, checkpoint system, new fixtures,
or unrelated optimization unless a concrete launch-blocking defect requires
it.  Do not edit implementation, run production/GHA, or perform git.

Write only `sol/sol_reply_638_audit_r07_task625_state_cap_terminal.md` with
`PASS_CAP_ONLY_RERUN`, `PASS_AFTER_REPAIR`, or `FAIL`, the exact evidence,
and `verified=false`.
