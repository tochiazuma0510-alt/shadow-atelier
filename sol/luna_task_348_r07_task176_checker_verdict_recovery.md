# Luna task 348 - recover the accepted task176 checker verdict as a physical owner

Role: Luna, bounded provenance recovery only. Do not run Python, Node, GAP,
GHA, a workflow, git, or network. Do not edit any existing file. The source
artifact was downloaded by the parent broker from immutable GitHub Actions run
`33044121344`, artifact id `9635036013`, name `gap-run-out`, at head
`0533e42019c9f67f6cec3d1566152db17b903836`. Its temporary extraction is the
newest directory matching
`$env:TEMP\shadow_atelier_task176_recovery_*`.

## 1. Read first

Read in full:

1. `sol/luna_reply_176_r07_all_seven_extension_section_census_v1.md`;
2. `ci/in/d972_r07_all_seven_extension_section_census_v1.manifest.json`;
3. the extracted `d972_r07_all_seven_extension_section_census_hashes_v1.txt`;
4. the extracted
   `d972_r07_all_seven_extension_section_census_crosscheck_v1.json`.

The accepted receipt manifest fixes run `33044121344`, artifact
`9635036013`, head `0533e420...`, and archive SHA-256
`250e25c992cbe8562f59fb808a8b0d86a7b54fdb750a57f2b1cd1c6cd0c89912`.
The accepted reply fixes the checker verdict at 757 bytes, SHA-256
`e6a45a34353ce1fb54c99b4f9cbc8b106f34bfc751dd50044f2a79da72cad5e5`,
and self digest
`e9d42ea064e7caaa9a333f7e2a8aec42f709bf1565e9fc9a8950ef92e18ce473`.
The extracted hashes file must independently contain the exact receipt and
verdict member hashes recorded there.

## 2. Sole permitted outputs

Create only these three new files:

- `ci/in/d972_r07_all_seven_extension_section_census_crosscheck_v1.json`;
- `ci/in/d972_r07_all_seven_extension_section_census_crosscheck_v1.recovery.manifest.json`;
- `sol/luna_reply_348_r07_task176_checker_verdict_recovery.md`.

Use `apply_patch` for file creation. Preserve the verdict bytes exactly,
including its final newline convention. Do not copy any log, command, empty
sentinel, receipt duplicate, or other artifact member.

## 3. Gates

Before writing, establish by read-only PowerShell checks that:

- the accepted local receipt and manifest still have their recorded byte/SHA
  identities;
- the extracted verdict has exactly the accepted byte/SHA/self-digest and
  contains `grade=CROSS_CHECKED`, the accepted terminal, receipt byte/SHA,
  producer SHA, and claim boundary;
- the physical producer and checker sources have SHA-256
  `878cf1d8d44e74a993309ed1c613c9fc57eb62fd2da48a30fd8797ff4b19af3b`
  and `4e6b97aa315fdccb4250de21e99dd78302477b90fd420215de6c6bea7d1fa695`;
- the extracted hashes file binds both receipt and verdict SHA exactly.

The recovery manifest must be one canonical one-line JSON object with a
self-digest (computed by deleting only the self-digest field before canonical
serialization). Record the run/head/artifact/archive identities, source temp
member names, accepted receipt manifest path/bytes/SHA, recovered verdict
path/bytes/SHA/self-digest, physical producer/checker paths/bytes/SHA, hashes
file bytes/SHA, and the accepted task176 reply path/bytes/SHA. It is a
provenance recovery record, not a new mathematical acceptance or execution.

After writing, re-read and hash both new machine files. If any identity or
semantic gate fails, create only the reply and return `BLOCKED / UNEXECUTED`.

## 4. Reply

Report exact bytes/SHA for the two machine files and every input checked.
State explicitly that no computation, checker rerun, workflow, network, or git
operation was performed by Luna, and that the mathematical grade remains the
already accepted task176 `CROSS_CHECKED` grade. End with exactly:

```text
RECOVERY:                       COMPLETE or BLOCKED
TASK176 MATHEMATICAL GRADE:     unchanged CROSS_CHECKED or UNKNOWN
A4 EFFECT:                      physical checker-result owner restored or NONE
EXECUTION:                      UNEXECUTED
LIFT / FAKE / IHARA:            NONE
```

`TASK348_R07_TASK176_CHECKER_VERDICT_RECOVERY`
