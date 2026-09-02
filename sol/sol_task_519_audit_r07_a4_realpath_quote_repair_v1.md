# Sol task 519 -- independent audit of A4 realpath quote repair

Role: independent Sol(max) implementation/provenance auditor.  Bounded audit
only: no production, GHA, workflow, git, release, or implementation edits.
Reply only to
`sol/sol_reply_519_audit_r07_a4_realpath_quote_repair_v1.md`.

## Frozen subjects

- v46: 12544 /
  `d3a864e47ebe0255221ccafee15b09925b2e1e462b21d8d0158c2d9c9e0f97e7`
- v47: `search/d972_r07_word_independent_successor_kernel_gha_driver_v47.g`
  - 12536 /
    `ba74cd1bb09bb87b50c582330bf54f943a5c4c1c77522a518460acf76a5748aa`
- Task518 reply: 986 /
  `ed0c837b2088eea122cd37b4c6a4d7387259196871b39ccc2a977beba72d4965`
- failed preflight run `33577179579`, job `100083610141`, exact v46 head
  `fafcd540635dd411bac54f9e914193d9b6e206e1`
- its downloaded artifact is outside the repository at
  `C:/Users/81905/AppData/Local/Temp/shadow-atelier-task518-a4-fail-9827064361`;
  generated v46 shell is 16065 /
  `1c03e4fb624cd9c374a6ac9eb6383a1a98857b970dbce21df19beb9b7fbac041`.

## Required audit

1. Recompute pins and query the failed run read-only.  Confirm it failed
   before curl/producer because generated v46 line 7 passed a filename with
   literal quote bytes to `realpath`.
2. Mechanically establish that v46-to-v47 has exactly one replaced source
   line, removing only the two emitted backslash-quote fragments around the
   static `D514Input` operand.  Reject any other change or padding.
3. Independently reconstruct/extract the v47 generated shell without executing
   it.  Confirm the exact line is
   `test "$(realpath -- ci/in/d972_r07_seven_context_roof_presentation_v1.json)" = "$root/ci/in/d972_r07_seven_context_roof_presentation_v1.json"`
   and that this realpath resolves to the checked-out regular input file.
4. Run only GAP `ReadAsFunction` and `bash -n` on a repository-external
   reconstructed shell.  Do not execute the production shell.
5. By exact one-line diff, confirm preservation of every Task516-GO gate and
   that v47 adds no rebuild, copy, retry, self-test, or traversal overhead.

Return `GO_FOR_GHA_REDISPATCH` or `STOP_DO_NOT_ADOPT`, with exact evidence and
reply bytes/SHA-256.  GO is transport-only and promotes no A4 claim.
