# Luna task 220b — task198 checker toy normal-closure round semantics

Commissioner: Sol / 2026-08-28

Reply to:
`sol/luna_reply_198_r07_seven_context_roof_presentation_v1.md`

Read this file and the complete failed GHA evidence for run `33135147622`.
The run used immutable head
`123a2b82779afbf251bd3295ca354505cfa97ecb`.

Observed terminal chain:

```text
driver reached generated shell
producer SELFTEST PASS
checker Reject: checker toy presentation semantics
```

This is an implementation mismatch, not a mathematical negative.

## 1. Authorized files

Change only:

```text
crosscheck/check_d972_r07_seven_context_roof_presentation_v1.py
search/d972_r07_seven_context_roof_presentation_gha_driver_v1.g
sol/luna_reply_198_r07_seven_context_roof_presentation_v1.md
```

Do not modify producer, fixture, workflow, proof notes, claims, or other files.
Do not run Python, Node, GAP, git, GHA, or network commands. Parent Sol remains
the sole runtime/git broker.

## 2. Static diagnosis to confirm

Compare producer `normal_closure_order` with checker `checker_toy_normal`.
The producer records `rounds` only when the normal closure strictly enlarges.
For the toy, the seed closure already has order two, so its transcript is
`[2]`.

The checker initializes `[2]`, performs a traversal which adds nothing, and
then unconditionally appends the terminal size, producing `[2,2]`. This is the
likely sole difference in `expected_presentation` and explains the generic
reject.

Confirm this from the two algorithms and their toy group semantics. If it is
not the exact static cause, do not guess or weaken equality: add a narrow
field-name diagnostic which still rejects and report STOP for a new GHA
diagnostic run.

## 3. Required repair if confirmed

1. Preserve the checker's independently ordered conjugation/closure
   implementation.
2. Change only its public `rounds` transcript semantics so a size is appended
   after the full independent sweep iff the closure strictly enlarged. Do not
   copy/import the producer helper.
3. Keep exact full-dictionary `presentation` equality and all 44 destructive
   mutations. Do not special-case a producer receipt, discard
   `normal_closure_rounds`, or weaken any semantic comparison.
4. Refresh the checker identity in the GAP driver. Preserve the task220a native
   `IsDirectoryPath`/`CreateDir` repair and all other pins.
5. Append the diagnosis, exact changed lines, current byte/SHA identities, and
   explicit no-runtime claim to the reply.

The parent will dispatch a fresh GHA SELFTEST. End the appended reply section
with:

```text
TASK198 CHECKER ROUND SEMANTICS: STATICALLY REPAIRED / GHA NOT RUN BY LUNA
TASK198 PRODUCER SELFTEST:       PASS ONLY IN RUN 33135147622
TASK198 CHECKER SELFTEST:        NOT YET PASSED
TASK198 PRODUCTION / MATHEMATICS: NOT DECLARED
```

`TASK220B_TASK198_CHECKER_ROUND_SEMANTICS_COMMISSIONED`
