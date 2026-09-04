# Luna Task899 -- physical state / canonical separator v1 against live v11 parent

You are Luna.  Begin the implementation specified in
`sol/luna_task_871_r07_physical_state_separator_v1.md`, with the exact parent
updates below.  That file's algorithm, resource discipline, tests, authorized
three outputs and claim boundary remain authoritative.  Do not use Git/GHA or
open production artifacts locally.

Replace its stale physical-v5 references by:

- accepted producer v6 and independent checker v7;
- Sol(max) release audits Task892 and Task896;
- workflow v11 and live run/attempt `33876776771/1`, head
  `b44ec9bd078ce0a6ca596a38cfea5012f4fee4d2`, job `101035535909`;
- connection/launch/checkpoint schemas v6; and
- accepted rho2 flat stager v4 plus Sol(max) Task894.

The v11 producer has completed successfully and the independent full replay
checker is running.  Implement the complete file-backed physical-state core,
target reduction, MEMBER back-substitution and v536 reverse-insertion-order
Separator now using bounded production-shaped fixtures.  Pivot leads are
unique normalized insertion-order leads; they are **not** numerically sorted.
Every prior pivot is replayed from its authenticated connection origin,
reductions and scale.

Do not invent, wildcard, or self-seal the not-yet-published final candidate
artifact tuple.  Centralize the final immutable run/artifact receipt and pause
only that binding until root sends the completed run's exact id/name/bytes/
digest/expiry.  Do not emit the final Luna reply or claim implementation ready
before that tuple is inserted and its ordinary path is tested.  Continue all
other implementation/tests in the meantime.  No workflow or joined CEGAR
loop belongs to this task.
