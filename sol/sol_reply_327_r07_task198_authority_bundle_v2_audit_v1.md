# Sol(max) reply 327 — task198 authority bundle v2 independent audit

## Verdict

**REJECT / UNEXECUTED.**  The corrected five-member authority bundle itself
passes every byte, seal, direct-run, verdict, source, presentation, normal-
generation, bridge, and false-witness check below.  The first and only
blocker is instead an exact inconsistency in the commissioned cross-capture
gate in task327 Section 3.

The preserved producer-only capture is present, so the optional-when-absent
comparison is applicable.  Removing **only** the top-level `resource` and
`self_digest_sha256` members from each receipt gives two exactly equal
31,016,535-byte canonical objects with common SHA-256

```text
8d6b9a7ed7d7ffaf61962678cd0e8bb3f4e6a219728c44cd1509e6c2cf2698ba
```

It does **not** give task323's reported 30,582,643-byte digest
`595dbe85...`.  That old byte count and digest are reproduced exactly only
by deleting the entire top-level `resume` member as well as `resource` and
`self_digest_sha256`:

```text
remove resource + self only:
  bytes  = 31,016,535
  sha256 = 8d6b9a7ed7d7ffaf61962678cd0e8bb3f4e6a219728c44cd1509e6c2cf2698ba

remove resource + resume + self:
  bytes  = 30,582,643
  sha256 = 595dbe85a9338ef77c694a31f62e456c5f49f6bd84263b8273bf21fb38238d19
```

Thus task323 Section 7's description of its own normalization was wrong,
and task327's demand that the correctly normalized object equal that old
digest cannot pass as written.  This is a reference-accounting defect, not a
mathematical difference between the two receipts: the stronger comparison
which retains the complete `resume` object succeeds byte-for-byte.  There
are no further bundle blockers.  Correcting the commissioned reference to
the 31,016,535-byte digest above would leave this bundle otherwise eligible
for `PASS / UNEXECUTED`.

Only read-only PowerShell byte/hash/JSON inspection was used.  Python, Node,
GAP, GHA, workflows, network, git, producer, and checker were not run.

## 1. Exact member identities

| member | bytes | SHA-256 |
|---|---:|---|
| receipt `d972_r07_seven_context_roof_presentation_v1.json` | 31,017,244 | `82f7955580039f2a0271896c928515d26996f636d8e73231331da6a37f6b19f5` |
| new manifest `d972_r07_seven_context_roof_presentation_v1.acceptance_v2.json` | 2,722 | `cc8c16c8ad8f2d094868f0897bcca2a98adba75c18bf7ff397f0da67fd233ea4` |
| producer attestation | 81 | `b5ab577d14ed490af12e3921ee41cfea533abcbf92d60cc037f0d40035ba5090` |
| checker attestation | 95 | `260eb23f73a8fb6b9cd2316aa4ea6c29a4a6db92e77d8c5c6f4f1dd6e7ff290e` |
| checker verdict | 150 | `ac841c5a979bbe89bdd47c73151ecabf29783793b7b288b4d08c4824596251de` |

The historical `acceptance.json` remains unchanged at 1,966 bytes and
SHA-256
`44ad985b20c7238e5aea661355b28b7c6b1100cd1e3947f7f23d8f658bf67903`.
It was not substituted for the new manifest.

The receipt, new manifest, and verdict all parse as JSON, are ASCII-only and
compact, and contain zero CR/LF and zero whitespace outside strings.  The
small new manifest and verdict also reproduce their input bytes exactly on
ordered compact reserialization.  The two attestations are the exact ASCII
terminal lines, each with one final LF and no CR:

```text
R07_SEVEN_CONTEXT_ROOF_PRESENTATION_V1_PRODUCER_TERMINAL ROOF_BRIDGE_ISOMORPHISM
R07_SEVEN_CONTEXT_ROOF_PRESENTATION_V1_CHECKER_PASS terminal=ROOF_BRIDGE_ISOMORPHISM rows=6441
```

Removing only the designated seal field independently gives:

```text
receipt self digest  = c8f7e65f6ec7553ab31928c911575de45fc0e3d70cd6e1d678bbebfee7502b9f
manifest self digest = 0f630669a906c93a3b7d40bd36633213316ff8da1b46ca254a552b3636963684
```

Each computed value equals its stored value.  Each seal field occurs exactly
once.

## 2. Complete direct-run and verdict binding

The new manifest has schema
`d972-r07-seven-context-roof-presentation/v1/acceptance-manifest/v3` and
binds all of the following exactly:

- top-level `accepted=true`, `independent=true`, and `synthetic=false`;
- producer and checker run `33155710862`, immutable head
  `bed1d5e6b41477b8799f2a33a24e46f7800f9510`, artifact `9686477718`, and
  archive digest
  `8e1d218cb3d0e09e7a633d2c7d4481f232b33e76eaafc51223c307a2c62e0854`;
- the same receipt basename, 31,017,244 bytes, file SHA, and receipt
  self-digest at the top level and in both producer/checker members;
- both attestation basenames, byte counts, SHA values, and the corresponding
  producer/checker terminal-line hashes; and
- checker-verdict basename, 150 bytes, SHA, schema, `accepted=true`,
  `independent=true`, and terminal `ROOF_BRIDGE_ISOMORPHISM`.

The checker verdict independently parses to exactly the four-field canonical
object

```json
{"accepted":true,"independent":true,"receipt_terminal":"ROOF_BRIDGE_ISOMORPHISM","schema":"d972-r07-seven-context-roof-presentation/v1/crosscheck/v2"}
```

and its complete semantic object equals the four semantic fields embedded in
the manifest.  The new manifest contains none of producer-only run
`33155653989`, artifact `9684074697`, or producer-only receipt SHA
`d4bccb2f...`; no capture identity was substituted for the direct run.

The three bound current source identities also independently match disk:

| source | bytes | SHA-256 |
|---|---:|---|
| `search/d972_r07_seven_context_roof_presentation_v1.py` | 137,169 | `6b2645b80f97256a659af81e856c086cca724b36e2a22ae70335b29ffa95d44c` |
| `crosscheck/check_d972_r07_seven_context_roof_presentation_v1.py` | 157,253 | `001277d44dbbc2acd7e03c6ecb6c6419df84996ae188cbb4be7b18f7cfb56ca1` |
| `search/d972_r07_seven_context_roof_presentation_gha_driver_v1.g` | 20,541 | `6048174be12d5f6f48508f1b2e80c87b3e1cb9df9ed348b30b6d3e19420b5068` |

All direct-run and verdict binding gates are **PASS**.

## 3. Receipt, rows, and seven chunks

The receipt envelope is exactly schema
`d972-r07-seven-context-roof-presentation/v1`, status `COMPLETE`, and terminal
`ROOF_BRIDGE_ISOMORPHISM`.  Direct parsing and a complete ordinal scan give:

```text
row_count / actual length = 6441 / 6441
Gamma_Cayley               = ordinals 1..6318
action                     = ordinals 1..104
Q0_lift                    = ordinals 1..19
ordinal mismatches         = 0
```

Hashing the exact 30,540,174-byte canonical `rows` array, independently of
the stored digest, gives

```text
e00880c01bc96ba8f0549311f4955662668d74001ecf5c06097646dad4268950
```

The array splits into all 6,441 rows and rejoins exactly.  Every
sealed chunk has `prefix_complete=true`; all seven canonical slice hashes
recompute exactly:

| interval | SHA-256 |
|---|---|
| `[0,1024)` | `0c0e58393e7a40dc9fe963865205c65e4c472f3b2dbef0f1e14b3f966d7384da` |
| `[1024,2048)` | `035c1f704201d59ac7a41900ecee592423bd1ab9890f753f9fb9f10a3b6bbc19` |
| `[2048,3072)` | `6752eb1dcfd14739ebf5fe15622cc98db49758843d4cb0b2e42df6569c099ca9` |
| `[3072,4096)` | `cde8b1e675484f074ab09e8a2478a2762abc5606c9969a553b909a63907d7881` |
| `[4096,5120)` | `3e300ea7b21f3a95c2ac25fa07d77e51a29296e534d891f017e19b9fa105655f` |
| `[5120,6144)` | `87862c1e0a531d663d2a6223042f2b8d4ddb575a2b2888629e11414023e0f8d6` |
| `[6144,6441)` | `5a4da210ce72a9194c2e9e8fc0e294846ab80362b9945aa8b0f48fe7ffeabb56` |

Hashing the exact canonical seven-chunk ledger gives
`8632f613886b4e2f70fc0b49dff0274122590ff3970a16d689c0d3c4507496aa`,
equal to `resume.chunks_sha256`.

## 4. Normal-generation and bridge proof replay

Every arithmetic and internal-binding gate in the authenticated proof payload
recomputes:

- `|Gamma|=243`, `|Q0|=1,469,664`, and
  `243 * 1,469,664 = 357,128,352 = |Delta0| = |D_all|`;
- Gamma has 243 Cayley states and `243*26=6318` Cayley edges; Q0 has
  1,469,664 states and 2,939,328 directed edges;
- the Q0 order proof has matching abstract/direct factor orders
  `2916` and `504`, with `2916*504=1,469,664`, nineteen complete relators,
  four cross commutators, and two marked splitting equations;
- selected records `[1,3,6,9]`, selected/all-record-generator closure order
  243, defect normal-closure rounds `[243]`, 19 Q0 lifts, 104 marked action
  loops, and all normal-closure Booleans agree;
- the presentation upper bound and surjective marked-image order are both
  357,128,352, so `upper_bound_equals_image_order=true` is arithmetically
  consistent; and
- the task157ee complete-relator and factor-payload digests agree with the
  normal proof.

The bridge has image order 357,128,352 and kernel order 1.  The ten-to-eleven
map, inverse deletion, and seven blocks recompute mutually:

```text
ten_to_eleven = 0,1,2,3,0,4,5,6,7,8,9
delete slots  = 0,1,2,3,5,6,7,8,9,10
block arities = 3,3,1,1,1,1,1
```

There are exactly seven blocks, eleven typed occurrences, eleven mapped
coordinates, and four marked inverse replays.  All occurrence ordinals,
block indices/slots, context ids, E3/E4 types, signs/orientations, and ten
indices agree with those maps.  The canonical occurrence ledger independently
hashes to
`040ab853535db8aad06fba295adf8b59bb1cd77435e7c64a1edcc34cdacb4cd7`.
All four marked word hashes and all left/regroup/image inverse flags replay
internally.

The exact 6,441-element bridge-digest array hashes to
`613b08a923d14571bdd1b898e45b951a7fa61ca196dae64c07a7636b175d306f`,
equal to both bridge relator-replay and resume digests; its count and
all-left-and-right-inverses flag agree.  The typed-coordinate digest
`9f9c081e9653d6e141e4d6d231e2d6db9526850b7ccd33c0859d13825f3fa83c`
agrees among bridge, evaluator, and the bound task176 input.  The evaluator
binds the v188 schema/callable, `load_runtime`, the row digest, and widths
`40,40,40,40,40,154,154,154,154,154`.

Finally, `cofinal_lift=false`, `fake=false`, and `Ihara_witness=false` are
present as actual Boolean false values.  No witness conclusion is smuggled
into this authority receipt.

## 5. Cross-capture erratum and scope

The producer-only capture found read-only under the preserved temporary
artifact is exactly 31,017,244 bytes with its recorded SHA-256
`d4bccb2f6443acde5ebe07c3648fc9a505315fd4b2eb00e6cdbad372fa9c5f4b`.
The correct normalization retaining `resume` proves exact equality of every
non-resource field, including the full resume transcript.  The task323
30,582,643-byte comparison was weaker because it accidentally discarded that
transcript.  This audit does not silently reinterpret task327's explicit
expected digest; it records the contradiction and rejects as commissioned.

```text
AUTHORITY BUNDLE V2:           REJECT / UNEXECUTED
A4 INPUT-AUTHORITY MILESTONE:  NOT ELIGIBLE; remains 0/3 under task327
A4 CONSUMER / PRODUCTION:      REJECTED / UNEXECUTED
LIFT / FAKE / IHARA:           NONE
FURTHER BUNDLE BLOCKERS:       NONE
```

This rejection does not reverse v264's cross-checked task198 presentation,
and it does not alter task323's independent rejection of the A4/v2 consumer.
After the normalization reference is corrected, a later PASS could advance
only A4's input-authority milestone to 1/3; it would still not authorize
SELFTEST, production, local evaluator construction, closure, K/anchor, lift,
fake, or Ihara claims.

`TASK327_R07_TASK198_AUTHORITY_BUNDLE_V2_INDEPENDENT_AUDIT`
