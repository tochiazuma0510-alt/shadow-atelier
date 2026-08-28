# R07 task198 authenticated production input v222

Author: Sol / 2026-08-28

Status: infrastructure provenance audit. This note binds the existing
cross-checked task176 production artifact to the exact `ci/in` names consumed
by task198. It makes no new finite-group or lift claim. Task198 production has
not yet been accepted in this note.

## 1. Source execution

The source is task176 GHA production run `33044121344` at immutable head

```text
0533e42019c9f67f6cec3d1566152db17b903836
```

Its producer and independent checker both returned
`R07_ALL_SEVEN_EXTENSION_SECTION_CENSUS_PASS`. The GHA artifact API currently
returns:

```text
artifact id       9635036013
artifact name     gap-run-out
artifact bytes    9276205
artifact digest   sha256:250e25c992cbe8562f59fb808a8b0d86a7b54fdb750a57f2b1cd1c6cd0c89912
expired           false
```

## 2. Payload identity

The artifact was downloaded outside the repository and the task176 receipt was
rehashed before copying. The source and staged destination agree exactly:

```text
path    ci/in/d972_r07_all_seven_extension_section_census_v1.json
bytes   13649089
sha256  715441d8ecb1b4bb39a51cf3df15f04d6179ee6adeafa5b925485dbbe91f7f41
```

These are the exact production-only values pinned by
`search/d972_r07_seven_context_roof_presentation_gha_driver_v1.g`.

The adjacent canonical staging manifest records the artifact ID, artifact ZIP
digest, run ID, full head, payload path, payload byte count, and payload SHA.
The task198 driver checks all of those immutable needles before producer
launch.

## 3. Scope boundary

This staging closes only the availability/authentication prerequisite for the
last v220-A1 milestone. It does not itself complete A1. A1 moves from 3/4 to
4/4 only if task198 producer and independent checker accept the actual 6,441
row roof presentation, or reaches a typed UNKNOWN state if a registered
resource/input boundary stops it.

```text
TASK176 INPUT IDENTITY:              AUTHENTICATED AND STAGED
TASK198 PRODUCTION INPUT AVAILABLE:  YES
TASK198 6,441-ROW PRODUCTION:         NOT YET ACCEPTED
ACTUAL SUCCESSOR K / POINTED MU1:     NOT COMPUTED
COMPATIBLE COFINAL LIFT / FAKE/IHARA: NOT DECLARED
```

`R07_TASK198_AUTHENTICATED_PRODUCTION_INPUT_V222_AUDIT_GRADE`
