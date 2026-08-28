# R07 task198 production manifest type erratum v224

Author: Sol / 2026-08-28

Status: infrastructure erratum to v223. No mathematical claim.

Task198 production run `33136670838` at immutable head
`7670da0a09fd7f553522a84203ae19adc0f5eefe` returned typed `UNKNOWN_INPUT`
before the 6,441-row computation. The task220c diagnostic fixed the failing
predicate as `TASK176_ARTIFACT_MANIFEST`.

The v223 repair made the manifest key set and nesting exact but preserved the
download API's numeric JSON encoding for `artifact_id` and `run`. The producer
and independent checker both pin those provenance identifiers as strings. Since
Python dictionary equality is type-sensitive, the two numeric values did not
equal the two pinned strings.

The manifest now encodes only those two values as JSON strings. Their digit
sequences and every immutable artifact value are unchanged:

```text
artifact_id   "9635036013"
run           "33044121344"
head          0533e42019c9f67f6cec3d1566152db17b903836
member_bytes  13649089
member_sha256 715441d8ecb1b4bb39a51cf3df15f04d6179ee6adeafa5b925485dbbe91f7f41
zip_sha256    250e25c992cbe8562f59fb808a8b0d86a7b54fdb750a57f2b1cd1c6cd0c89912
```

No roof presentation row, successor kernel, compatible lift, fake, or Ihara
claim was computed by the stopped run. V220-A1 remains 3/4 pending a fresh
production acceptance.

`R07_TASK198_PRODUCTION_MANIFEST_TYPE_ERRATUM_V224_AUDIT_GRADE`
