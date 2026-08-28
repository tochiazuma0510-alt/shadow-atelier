# R07 task198 production manifest erratum v223

Author: Sol / 2026-08-28

Status: infrastructure erratum to v222. No mathematical claim.

Task198 production run `33135921512` at immutable head
`3d8063d0c96165141347849fdae758dcf9371f26` reached producer terminal
`UNKNOWN_INPUT` before the 6,441-row computation. The checker consistently
accepted the same typed nonpositive terminal; the driver then failed closed
because production promotes only `ROOF_BRIDGE_ISOMORPHISM`.

Static comparison with `authenticate_task176_receipt` identifies the staging
error. V222's first manifest contained all immutable values but nested them
under descriptive keys. The producer requires exact equality with the seven-key
dictionary

```text
artifact_id
zip_sha256
run
head
member
member_bytes
member_sha256
```

The manifest is corrected to that exact dictionary, with unchanged artifact,
head, payload byte count, and payload SHA values. The 13,649,089-byte task176
receipt itself was correct and is unchanged.

```text
RUN 33135921512:                  PRECOMPUTATION UNKNOWN_INPUT
TASK176 PAYLOAD IDENTITY:         UNCHANGED / AUTHENTICATED
STRICT SEVEN-KEY MANIFEST:        REPAIRED
TASK198 6,441-ROW PRODUCTION:     NOT REACHED
V220-A1:                          3/4
MATHEMATICAL NEGATIVE:            NONE
```

`R07_TASK198_PRODUCTION_MANIFEST_ERRATUM_V223_AUDIT_GRADE`
