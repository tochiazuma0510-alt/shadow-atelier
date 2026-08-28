# Luna task 220c — task198 exact task176 terminal binding

Commissioner: Sol / 2026-08-28

Reply to:
`sol/luna_reply_198_r07_seven_context_roof_presentation_v1.md`

Production run `33136073742` at immutable head
`7e35b0944fb315450d9a693355f8a26bcd59c3c8` again returned typed
`UNKNOWN_INPUT` before the 6,441-row computation.

## 1. Static diagnosis

The authenticated 13,649,089-byte task176 receipt has:

```text
schema    d972-r07-all-seven-extension-section-census/v1
status    COMPLETE
terminal  R07_ALL_SEVEN_EXTENSION_SECTION_CENSUS_PASS
```

Its bytes/SHA and self digest are the accepted task176 production identities.
However, both task198 producer `authenticate_task176_receipt` and independent
checker task176 authentication currently require
`terminal == "COMPLETE"`. The status and terminal fields were conflated.

## 2. Authorized files

Change only:

```text
search/d972_r07_seven_context_roof_presentation_v1.py
crosscheck/check_d972_r07_seven_context_roof_presentation_v1.py
search/d972_r07_seven_context_roof_presentation_gha_driver_v1.g
sol/luna_reply_198_r07_seven_context_roof_presentation_v1.md
```

Do not modify the task176 receipt, manifest, fixture, workflow, proof notes,
claims, or any other file. Do not run Python, Node, GAP, git, GHA, or network.
Parent Sol is the only runtime/git broker.

## 3. Required repair

1. Keep `status == "COMPLETE"` and bind `terminal` exactly to
   `R07_ALL_SEVEN_EXTENSION_SECTION_CENSUS_PASS` in both producer and checker.
2. Do not accept an alternate terminal, omit terminal checking, or weaken any
   task176 semantic/self-digest/bytes/SHA gate.
3. Preserve independent implementations; do not import the producer helper in
   the checker.
4. Add a separate producer diagnostic line for a nonpositive production
   envelope which prints the typed `reason` before the existing exact terminal
   marker. This is diagnostic only and must not change receipt bytes, terminal,
   exit code, or positive marker grammar.
5. Refresh producer/checker pins in the GAP driver. Preserve the native
   directory repair, checker round repair, 43-member cone, and all other pins.
6. Append the exact diagnosis, changed lines, and current byte/SHA identities
   to the reply. State that a new GHA SELFTEST and PRODUCTION run are required.

End with:

```text
TASK176 STATUS/TERMINAL TYPE SEPARATION: STATICALLY REPAIRED
TASK198 PRODUCER/CHECKER SELFTEST:       NOT RUN AFTER THIS REPAIR
TASK198 6,441-ROW PRODUCTION:            NOT REACHED
V220-A1:                                 3/4
MATHEMATICAL NEGATIVE:                   NONE
```

`TASK220C_TASK198_TASK176_TERMINAL_BINDING_COMMISSIONED`
