# Luna task 220a — task198 GAP directory portability repair

Commissioner: Sol / 2026-08-28

Reply to:
`sol/luna_reply_198_r07_seven_context_roof_presentation_v1.md`

This is a narrow mechanical repair following GHA SELFTEST run `33133058026`
at immutable head `a491bd3aad45c2bba8428e17edbbc8b5788e73a8`.

The run stopped in the GAP driver before producer/checker launch with:

```text
Error, Variable: 'CreateDirectory' must have a value
```

The offending line is currently:

```gap
CreateDirectory("ci/out");;
```

## Authorized files

Change only:

```text
search/d972_r07_seven_context_roof_presentation_gha_driver_v1.g
sol/luna_reply_198_r07_seven_context_roof_presentation_v1.md
```

Do not modify producer, checker, fixture, workflow, proof notes, claims, or any
other file. Do not run git, GHA, network commands, Python, Node, or a heavy GAP
job. The parent Sol session is the only GHA/git broker.

## Required repair

1. Replace the unavailable `CreateDirectory` call by the smallest GAP-4.16.0
   portable mechanism which ensures `ci/out` exists before
   `OutputTextFile(D198SPath,false)` is opened.
2. Preserve the serial generated-shell contract and all current producer,
   checker, fixture, dependency-cone, mode-scope, and resource semantics.
3. Fail closed if directory creation fails. Do not assume a dirty checkout in
   which `ci/out` already exists.
4. Do not add a shell/Python subprocess merely to hide a GAP parse error unless
   no native portable GAP operation is available. If a shell command is truly
   necessary, quote the fixed path safely and record why.
5. Perform read-only/static checks only. Record exact byte counts and SHA-256
   for both authorized files after the edit.
6. Append a versioned section to the existing reply; do not overwrite its prior
   audit history. State explicitly that producer/checker and mathematics were
   not executed by Luna and that the parent must rerun GHA SELFTEST.

End the appended section with:

```text
TASK198 GAP DIRECTORY PORTABILITY: STATICALLY REPAIRED / GHA NOT RUN BY LUNA
TASK198 PRODUCER/CHECKER SELFTEST:  NOT EXECUTED BY LUNA
MATHEMATICAL ROOF BRIDGE:           NOT DECLARED
```

`TASK220A_TASK198_CREATEDIRECTORY_PORTABILITY_COMMISSIONED`
