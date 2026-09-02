# Sol reply 517 -- independent A0 rank111 artifact audit

## Verdict

**GO_FOR_PREFIX_PROMOTION_AND_ARCHIVE.**

The immutable continuation prefix may be archived and promoted only as
**68 literal rungs / physical rank 111 / round 73**.  This is a
cross-checked stable prefix, not a positive A0 result and not Lean-verified.
The terminal remains
`UNKNOWN_RESOURCE:tau_free_formula_seed:time_limit`; all five mathematical
claims are false.

## External identity and exact code pins

A fresh unauthenticated read-only GitHub API query returned exactly:

- run `33564845217`, attempt 1, event `workflow_dispatch`, head
  `c582f8d786012a668783790007b72c5c422c3db8`, `completed/success`;
- its sole job `100045550767`, name `gap`, the same run/head, and
  `completed/success`;
- its sole artifact `9826862037`, name `gap-run-out`, `expired=false`,
  workflow-run owner `33564845217`, API size `96198`, and service digest
  `sha256:22aa0d836298e01fa27b2d893427839b18fe51a83781a840d357a1243e6d412c`.

The Contents API at that exact head reproduced these executable pins:

| object | bytes | SHA-256 |
|---|---:|---|
| producer v3 | 12,215 | `0140447110cfa568a77300bd7d43d51c622597704b7b91ed5209c63168c9ef37` |
| checker v7 | 3,653 | `e1b80c586985f5113b300508f6bc78d055a37243e3fd6795b8f81148b0988de1` |
| resume driver v10 | 8,662 | `8903f315e26b909791dead7673c4eef358c3cca7a2ddba7871476a477d8c3d1e` |

The exact v10 driver names the v7 checker and pins the first two hashes above
before invocation.  The artifact's 128-byte `driver.g` is the v10 wrapper and
has SHA-256
`393794cf2188ac0a27abe472180ddabca42e7f88082248726e4ae664cd371978`.
Thus the observed checker terminal belongs to the checker pinned by the
executed head and driver, rather than to an unbound checker copy.

## Archive and member recomputation

I read every ZIP entry as a stream and compared its bytes with the extracted
copy.  The current artifact has exactly eight distinct regular entries:

| member | bytes | SHA-256 |
|---|---:|---|
| rank98 input checkpoint | 69,947 | `c0fcb581f59c9ed665cf13cb852cb527ef13acdc9bf2102b89c2404bb080d37f` |
| preflight log | 38 | `52f94358c40a2e6968927b4078a0bf00b6a40c32eb013367679e8d59b599240c` |
| result v10 | 86,354 | `39434b6a4c1a7851805c2deb3be8de4e7e919085a537b8d3913a15d341c19279` |
| checker log | 51 | `aa62a0439618247aff32657b3d05d6c5d104340d161c0aa1b7fafac0b373f7b1` |
| output checkpoint | 85,934 | `69a7ec3da4907f24af0f68c1975538b9ff9b6102f14e334f7c0725d2542dfd93` |
| producer log | 4,905 | `271d05e70153cbceadf9d45478a4357bcd7899610b3857b3525644205b7e975c` |
| `driver.g` | 128 | `393794cf2188ac0a27abe472180ddabca42e7f88082248726e4ae664cd371978` |
| `run.log` | 5,004 | `ac7fcf963237cc23d88774df9c85d82cb8b3acc09f24b0ee4dda5506e719bf15` |

The downloaded prior-release ZIP is 30,758 bytes with SHA-256
`d0293cdd3bab98b792af17064ace21594966a5610e30219842347466e9ade9e4`.
Its eight distinct regular entries also equal their extracted copies:

| prior member | bytes | SHA-256 |
|---|---:|---|
| rank84 input checkpoint | 52,707 | `eb1a6d69a855b88d2a934dbf8e58c0f539a7a4d6802cc4a5c7f544b0880da24f` |
| rank84 preflight log | 35 | `4d3dd0892debc756d57c12ab585ff63d473aad334bf25339c3fe3af6cef79139` |
| result v9 | 70,365 | `2bbe05d8c5c2b97177854e7cd77944e9b89af70cea7f50e7565a6faec3a70b1d` |
| checker log | 51 | `aa62a0439618247aff32657b3d05d6c5d104340d161c0aa1b7fafac0b373f7b1` |
| output checkpoint v9 | 69,947 | `c0fcb581f59c9ed665cf13cb852cb527ef13acdc9bf2102b89c2404bb080d37f` |
| producer log v9 | 4,989 | `d585eec9c9b2f81a5689749ddc9fbe9d9e5e658651907ae95baf41d8827082fa` |
| `driver.g` | 126 | `ee8f36e711d719244b40b283f8d9debcdfd553b4ca0bee8dedcade6cd6ac8081` |
| `run.log` | 5,087 | `d2c1cc146af7b1af3eddfbd213b29ee2b75e8b8030a77dcff2747dbb9ff2dc7c` |

In particular, the current rank98 input and the prior v9 output are identical
bytes, not merely equal parsed objects.

## Prefix, seals, and terminal boundary

Independent ASCII-JSON parsing and canonical recomputation established:

- checkpoint binding
  `6f179b061a010bb2a9b427dda6564c7418b18f44da17ea2f28e9e080655326a3`;
- input `rank/count/round = 98/55/59`, with internal state seal
  `7fd45ecad90fda912df5dfdb15f2f422aa63dc8a3abfc992150079b44405685a`;
- output `rank/count/round = 111/68/73`, with internal state seal
  `3e0d4bc8e2f9a467a0e50ad8435a7360e1953c2baee369225d8aa6fd71379610`;
- exact JSON equality of the first 55 source records.  Their independently
  canonicalized list hash is
  `9c5abed433d1858287610823d1a163b8fa025e041ebe40ec1338f16487411297`
  on both sides;
- exactly 13 appended records, rounds 60 through 72 and ranks 98 through
  111, with canonical list hash
  `86b9cc29ee84baf7b3bd01fd5fc99d920ad22b3b0e201a0c50f599b2b1cd462f`.

All 68 records have the exact 20-field correction schema and satisfy the
frozen checker types for digest, pivot, scalar, rank transition, seed,
delta-word, exponent pair, coordinate, cursor, and required-coordinate data.
All 68 canonical records, pivots, and row digests are pairwise distinct; rank
transitions are exactly `43 -> 44` through `110 -> 111`.

The result's accepted list, count, rank, round, reason, and current-dual
profile equal the sealed checkpoint fields.  Its durable envelope binds
exactly 85,934 bytes and checkpoint SHA-256 `69a7ec...fd93`, count 68 and rank
111.  `terminal_replay` is null.  Status and terminal are both
`UNKNOWN_RESOURCE`, the reason is exactly
`UNKNOWN_RESOURCE:tau_free_formula_seed:time_limit`, and claims are exactly
`A0=false`, `COMMON=false`, `NONMEMBER=false`, `fake=false`, and
`Ihara=false`.

The producer log has exactly one
`R07_A0_ACTUAL_TAU_FREE_RANK_LADDER_V3 status=UNKNOWN_RESOURCE`; the checker
log is exactly one v7 PASS line; and `run.log` has exactly one each of that
producer terminal, the v7 checker PASS, and
`R07_A0_RANK98_CHECKPOINT_RESUME_V10_DRIVER_PASS`.  The complete retained
logs contain no `Traceback`, `ERROR`, `UNKNOWN_INPUT`, plain `UNKNOWN`,
positive/COMMON terminal, or A0 claim.

## Independent checker assessment and archival scope

The authenticated GHA job executed the exact pinned independent v7 checker
and retained its unique PASS.  That checker first enforces its frozen rank68
prefix and then performs the inherited independent semantic replay, sealed
checkpoint/result binding, profile, resource-boundary, rank, and claim checks
before printing PASS.  The separate audit above supplements it with the
commissioned exact rank98 55-record prefix equality.

A local duplicate replay was started, but Windows correctly hit the frozen
dependency's fail-closed same-handle portability boundary.  An audit-only
same-handle adapter would still require repeating the approximately
GHA-scale semantic computation.  It was intentionally terminated rather
than waste local Python resources or misrepresent an adapted run as an exact
Linux rerun.  This does not erase the authenticated exact-checker execution
inside the frozen successful GHA job; the independent API, archive, seal,
binding, prefix, type, distinctness, and terminal checks above do not rely on
the uploaded PASS text alone.  Any desired second full semantic execution
belongs on GHA.

The checkpoint is therefore a closed, continuation-ready RESOURCE prefix:
its predecessor is byte-identical to the archived rank98 state, its complete
accepted list and terminal state are canonically sealed, and result and
checkpoint are mutually bound.  Archival must not relabel it as a positive
boundary.  A0 remains `0/1 actual`; no COMMON, NONMEMBER, lift, fake, or Ihara
witness is declared.

The mathematics does not change.  This audit promotes only the provenance
status of the finite rank111 prefix to cross-checked and archivable.  The
final physical bytes/SHA-256 of this reply are supplied after freeze in the
parent delivery envelope because embedding its own digest would be
self-referential.

GO_FOR_PREFIX_PROMOTION_AND_ARCHIVE
