# Luna task 518 -- A4 realpath generated-shell quote repair

Role: Luna implementation only.  No production traversal, GHA, workflow, git,
release, or unrelated edits.  Reply only to
`sol/luna_reply_518_r07_a4_realpath_quote_repair_v1.md`.

## Frozen input and observed failure

- v46: `search/d972_r07_word_independent_successor_kernel_gha_driver_v46.g`
  - 12544 bytes
  - SHA-256 `d3a864e47ebe0255221ccafee15b09925b2e1e462b21d8d0158c2d9c9e0f97e7`
- GHA run `33577179579` reached the generated shell and failed before curl or
  production with exactly:
  `realpath: '"ci/in/d972_r07_seven_context_roof_presentation_v1.json"': No such file or directory`.
- Cause: the v46 GAP string emits backslash-escaped quote characters around
  the realpath operand, so bash passes literal quote bytes as part of the
  filename.

## Required one-line repair

Create versioned
`search/d972_r07_word_independent_successor_kernel_gha_driver_v47.g` from
v46.  Change only the `realpath --` generated-shell fragment so the operand is
the actual static safe path `ci/in/d972_r07_seven_context_roof_presentation_v1.json`,
not a filename containing quote characters.  For example, emitting
`realpath -- ci/in/...json` inside the quoted command substitution is valid.

Preserve every other byte and every v46 gate.  Do not rename Task514 markers
or outputs.  The exact v46-to-v47 diff must be one replaced source line only.

Bounded checks only:

1. GAP `ReadAsFunction` parse.
2. Independently reconstruct or extract the generated shell without executing
   it and show the exact corrected `realpath` command.
3. `bash -n` on that generated shell in a repository-external temporary
   directory; do not execute the shell.
4. Confirm diff confinement and report exact bytes/SHA-256.

No extra self-tests or refactoring.
