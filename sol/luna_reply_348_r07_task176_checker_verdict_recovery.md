# Luna reply 348: R07 task176 checker-verdict recovery

Date: 2026-08-29

## Disposition

Recovery is complete.  The accepted task176 checker verdict was recovered as a
physical checked-in owner from the newest extracted directory
`C:\Users\81905\AppData\Local\Temp\shadow_atelier_task176_recovery_7487cad74a15458d8b543e18f1a2a4e7`.
Only the verdict member was copied; no log, command, empty sentinel, receipt
duplicate, or other artifact member was copied.

## Inputs read and checked

Every numbered section of the task176 reply (Sections 1--8 and the parent
execution addendum) was read in full.  The task mail and all identity-bearing
inputs were checked with read-only PowerShell:

```text
sol/luna_task_348_r07_task176_checker_verdict_recovery.md
  bytes 3851
  sha256 ac720950533f3d8d436a97443ce1cc97034f11525482f2b956dbcdc259099132

sol/luna_reply_176_r07_all_seven_extension_section_census_v1.md
  bytes 47164
  sha256 aa173122310e33910d546bd3e02a98a6bf16aea9d3aad066b7d49976098ebb0c

ci/in/d972_r07_all_seven_extension_section_census_v1.manifest.json
  bytes 349
  sha256 de62e5e55a2e348a3cce297764f7ff4bfedc10ebe2545f22cbc1551f15e1adc1

ci/in/d972_r07_all_seven_extension_section_census_v1.json
  bytes 13649089
  sha256 715441d8ecb1b4bb39a51cf3df15f04d6179ee6adeafa5b925485dbbe91f7f41
  terminal R07_ALL_SEVEN_EXTENSION_SECTION_CENSUS_PASS
  receipt self_digest_sha256 f8f0ce249ff547d3e1235bd4b9760daa2b34f23771bf7da47b48dbd5cbbfae1d

search/d972_r07_all_seven_extension_section_census_v1.py
  bytes 66109
  sha256 878cf1d8d44e74a993309ed1c613c9fc57eb62fd2da48a30fd8797ff4b19af3b

crosscheck/check_d972_r07_all_seven_extension_section_census_v1.py
  bytes 84980
  sha256 4e6b97aa315fdccb4250de21e99dd78302477b90fd420215de6c6bea7d1fa695

TEMP source member d972_r07_all_seven_extension_section_census_hashes_v1.txt
  bytes 261
  sha256 c7cc68fd3e57e42fa03c85190c3c85f10f41b368d4a0182b0c25711fe36b933a

TEMP source member d972_r07_all_seven_extension_section_census_crosscheck_v1.json
  bytes 757
  sha256 e6a45a34353ce1fb54c99b4f9cbc8b106f34bfc751dd50044f2a79da72cad5e5

TEMP source member d972_r07_all_seven_extension_section_census_v1.json
  bytes 13649089
  sha256 715441d8ecb1b4bb39a51cf3df15f04d6179ee6adeafa5b925485dbbe91f7f41
```

The accepted receipt manifest binds run `33044121344`, head
`0533e42019c9f67f6cec3d1566152db17b903836`, artifact `9635036013`, member
`d972_r07_all_seven_extension_section_census_v1.json`, and archive SHA-256
`250e25c992cbe8562f59fb808a8b0d86a7b54fdb750a57f2b1cd1c6cd0c89912`.
The extracted hashes file independently binds the exact receipt and verdict
SHA-256 values above.  The extracted verdict contains terminal
`R07_ALL_SEVEN_EXTENSION_SECTION_CENSUS_PASS`, receipt bytes `13649089`, the
accepted receipt SHA, producer SHA, claim boundary
`no all-seven solution/correction/cofinal/fake/Ihara`, and grade
`CROSS_CHECKED`.

## Recovered outputs

```text
ci/in/d972_r07_all_seven_extension_section_census_crosscheck_v1.json
  bytes 757
  sha256 e6a45a34353ce1fb54c99b4f9cbc8b106f34bfc751dd50044f2a79da72cad5e5
  self_digest_sha256 e9d42ea064e7caaa9a333f7e2a8aec42f709bf1565e9fc9a8950ef92e18ce473

ci/in/d972_r07_all_seven_extension_section_census_crosscheck_v1.recovery.manifest.json
  bytes 2035
  sha256 41d2cb72614ce7e2d5b2d7a9000e861414da1c749876b3d51f1ccf2ca63390a8
  self_digest_sha256 f8c6c0faf2588cd58d8a2aec75a2a1f9950ea67769dd913fbd796d018098f581
```

The recovered verdict is byte-for-byte identical to the extracted verdict and
retains its final LF.  The recovery manifest is one canonical one-line JSON
object with a final LF; deleting only its top-level self-digest field and
hashing the canonical JSON body (1946 UTF-8 bytes) reproduces
`f8c6c0faf2588cd58d8a2aec75a2a1f9950ea67769dd913fbd796d018098f581`.
It records the run/head/artifact/archive identities, all three TEMP source
member names, accepted receipt and manifest identities, recovered verdict
identity, producer/checker identities, hashes-file identity, and accepted
task176 reply identity.

No computation, checker rerun, workflow, network, or git operation was
performed by Luna; only the required read-only byte/hash/schema gates were
used.  This recovery is provenance ownership restoration, not a new
mathematical acceptance or execution.  The mathematical grade remains the
already accepted task176 `CROSS_CHECKED` grade.

RECOVERY:                       COMPLETE
TASK176 MATHEMATICAL GRADE:     unchanged CROSS_CHECKED
A4 EFFECT:                      physical checker-result owner restored
EXECUTION:                      UNEXECUTED
LIFT / FAKE / IHARA:            NONE

`TASK348_R07_TASK176_CHECKER_VERDICT_RECOVERY`
