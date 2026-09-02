# Sol(max) reply 530 -- independent A0 rank143 artifact audit

## Verdict

**GO_FOR_PREFIX_PROMOTION_AND_ARCHIVE.**

The closed continuation-ready prefix may be promoted only as **100 literal
rungs / physical rank 143 / accepted through round 105, with checkpoint
cursor round 106**.  It is a cross-checked stable prefix, not a positive A0
result and not Lean-verified.  A0 remains `0/1 actual`; no COMMON, NONMEMBER,
compatible lift, fake, or Ihara witness is declared.

## F1. External identity and exact executable binding -- PASS

Fresh read-only GitHub API queries returned exactly:

- run `33579991982`, attempt 1, event `workflow_dispatch`, workflow
  `.github/workflows/gap-run.yml`, head branch
  `sol/r07-explicit-lift-20260825`, head
  `ae74e865ec7ba10d00eca263356afa01d23a2466`, and
  `completed/success`;
- exactly one job, `100092032846`, name `gap`, run/head/attempt as above and
  `completed/success`;
- exactly one artifact, `9831153395`, name `gap-run-out`, `expired=false`,
  workflow-run owner/head as above, API size `121469`, and GitHub service
  digest
  `sha256:6cf80ac0e37955174333f69a3e3b20c3026a957d12e20c2f53c29e1f2c62eeb9`.

The commit API returned that exact remote commit and tree
`123a02d210b382434a38f17637920d43ddd9c96e`.  The GHA checkout log records
the exact fetch and checkout of `ae74e865...a2466`.  The execution-step log
then records exactly this invocation:

```text
GAP_RUN_SCRIPT:   search/d972_r07_a0_actual_tau_free_rank111_resume_gha_driver_v11.g
GAP_RUN_PREAMBLE: D972_R07_A0_RANK111_CHECKPOINT_RESUME_V11_RUN:=true;;
GAP_RUN_OUT_DIR:  ci/out
```

The Contents API blob identities at that head agree with the exact local Git
object, from which I independently recomputed these byte/SHA-256 pins:

| exact-head object | bytes | SHA-256 |
|---|---:|---|
| generic `gap-run.yml` | 13,309 | `0c2ba9089d7e43d9d34d43afa039618a354307037ddf9ea332535e43a70cecae` |
| rank111 resume driver v11 | 8,683 | `84db6c150d8ce764c411afa91a9cc9c31ad193ecaf719900faa9ebdbc32b5b7d` |
| producer v3 | 12,215 | `0140447110cfa568a77300bd7d43d51c622597704b7b91ed5209c63168c9ef37` |
| independent checker v7 | 3,653 | `e1b80c586985f5113b300508f6bc78d055a37243e3fd6795b8f81148b0988de1` |
| producer dependency v2 | 18,191 | `cd27d69b06538e77dac1963d147f4966d8f63b9bf0d9e54860f2dae69149369b` |

The artifact's 130-byte `driver.g`, SHA-256
`ee902189e30d6355e2be449a8a0b3f9af666943c86b011040ae674ca1c1fbefa`,
is exactly the two-line wrapper for that v11 driver and preamble.  The v11
driver checks the producer and checker byte/SHA pins before invoking either.
The result in turn pins producer v2 to the final row of the table.  Checker v7
loads its independently pinned v6-to-v2 checker chain and frozen rank68 state
before it can print PASS.  Thus the retained v7 marker belongs to the exact
checker executed at the authenticated head, not merely to an uploaded marker
file with no code identity.

## F2. Complete extracted inventory -- PASS, with explicit addendum

No byte count or digest in the frozen **principal-member** inventory needs
correction.  That list is not a complete regular-member manifest: the
extracted artifact has 17 regular files, no reparse points, and 642,851 total
uncompressed bytes.  The completeness addendum consists of the current
preflight log plus the eight expanded prior-archive files.  A sorted
`relative-path<TAB>bytes<TAB>sha256<LF>` manifest is 2,410 bytes with SHA-256
`e697272174c3f37f1b6d9e30dba8628cca670753d287e2d96e01898f5ba72d3e`.

The complete current layer is:

| regular member | bytes | SHA-256 |
|---|---:|---|
| `d972_r07_a0_actual_tau_free_rank_ladder_v11.json` | 126,799 | `8c7072c3702d281994a57ec9f18f9b02716c64b06ebd97841685f5903b47835d` |
| `d972_r07_a0_actual_tau_free_rank_ladder_v11_checker.log` | 51 | `aa62a0439618247aff32657b3d05d6c5d104340d161c0aa1b7fafac0b373f7b1` |
| `d972_r07_a0_actual_tau_free_rank_ladder_v11_output.checkpoint` | 126,377 | `dff9cb181ae40abfac23ccba1b7c819ad353ecbec3825e5922e944dbe4b41b4c` |
| `d972_r07_a0_actual_tau_free_rank_ladder_v11_producer.log` | 6,737 | `5c5a886e7e060ee9f80d85f02a559b544cee0421be6f86142d98953a6914a654` |
| `d972_r07_a0_actual_tau_free_rank111_resume_v11.zip` | 37,586 | `8b740dbbc81f5d2e659371a81453ded56c6711ce8ace35a4af5255303e0095de` |
| `d972_r07_a0_actual_tau_free_rank111_resume_v11_input.checkpoint` | 85,934 | `69a7ec3da4907f24af0f68c1975538b9ff9b6102f14e334f7c0725d2542dfd93` |
| `d972_r07_a0_actual_tau_free_rank111_resume_v11_preflight.log` | 39 | `d788b727ab5b162db6ba42529135e393cd570d66eceb08b7a443f20fea7bbf74` |
| `driver.g` | 130 | `ee902189e30d6355e2be449a8a0b3f9af666943c86b011040ae674ca1c1fbefa` |
| `run.log` | 6,837 | `596e8f35fad264d610474f0e9ea60684d389ffb8909ea5a19deb6b12d11a9eda` |

Under
`d972_r07_a0_actual_tau_free_rank111_resume_v11_archive/`, the other eight
regular members are:

| archived regular member | bytes | SHA-256 |
|---|---:|---|
| `d972_r07_a0_actual_tau_free_rank_ladder_v10.json` | 86,354 | `39434b6a4c1a7851805c2deb3be8de4e7e919085a537b8d3913a15d341c19279` |
| `d972_r07_a0_actual_tau_free_rank_ladder_v10_checker.log` | 51 | `aa62a0439618247aff32657b3d05d6c5d104340d161c0aa1b7fafac0b373f7b1` |
| `d972_r07_a0_actual_tau_free_rank_ladder_v10_output.checkpoint` | 85,934 | `69a7ec3da4907f24af0f68c1975538b9ff9b6102f14e334f7c0725d2542dfd93` |
| `d972_r07_a0_actual_tau_free_rank_ladder_v10_producer.log` | 4,905 | `271d05e70153cbceadf9d45478a4357bcd7899610b3857b3525644205b7e975c` |
| `d972_r07_a0_actual_tau_free_rank98_resume_v10_input.checkpoint` | 69,947 | `c0fcb581f59c9ed665cf13cb852cb527ef13acdc9bf2102b89c2404bb080d37f` |
| `d972_r07_a0_actual_tau_free_rank98_resume_v10_preflight.log` | 38 | `52f94358c40a2e6968927b4078a0bf00b6a40c32eb013367679e8d59b599240c` |
| `driver.g` | 128 | `393794cf2188ac0a27abe472180ddabca42e7f88082248726e4ae664cd371978` |
| `run.log` | 5,004 | `ac7fcf963237cc23d88774df9c85d82cb8b3acc09f24b0ee4dda5506e719bf15` |

Direct ZIP streaming found exactly eight unique regular entries in the
37,586-byte prior-release ZIP.  Every entry is byte-identical to the matching
expanded archive file.  In particular, the copied rank111 input is
byte-identical to the archived v10 output checkpoint, not just equal after
JSON parsing.

## F3. Exact terminal cardinality and negative boundary -- PASS

The current invocation's terminal channels are the top-level producer,
checker, and run logs; the nested `..._archive/` logs are immutable input
lineage and are not a second execution of this continuation.

- The 6,737-byte producer log has 78 lines, exactly 32 progress lines, exactly
  one gate
  `UNKNOWN_RESOURCE:tau_free_formula_seed:time_limit rank=143`, and exactly
  one producer terminal
  `R07_A0_ACTUAL_TAU_FREE_RANK_LADDER_V3 status=UNKNOWN_RESOURCE`.
- The 51-byte checker log is exactly the single line
  `R07_A0_ACTUAL_TAU_FREE_RANK_LADDER_V7_CHECKER_PASS`.
- The 6,837-byte `run.log` is byte-for-byte the producer log followed by that
  one checker line and one
  `R07_A0_RANK111_CHECKPOINT_RESUME_V11_DRIVER_PASS` line.  It therefore has
  exactly one of each commissioned terminal.
- The 39-byte preflight log is exactly one BEGIN line and has no FAIL line.

Scanning every non-ZIP regular payload, including the expanded ZIP contents,
found no `Traceback`, `ERROR`, `UNKNOWN_INPUT`, exact plain-`UNKNOWN` JSON or
log terminal, positive/COMMON terminal, or true A0/COMMON claim.  The current
result has `status=terminal=UNKNOWN_RESOURCE`, exact reason
`UNKNOWN_RESOURCE:tau_free_formula_seed:time_limit`, null `terminal_replay`,
and claims exactly
`A0=false`, `COMMON=false`, `NONMEMBER=false`, `fake=false`, and
`Ihara=false`.

## F4. Independent state, prefix, and structural audit -- PASS

Independent ASCII-JSON parsing and canonical serialization established that
the input, result, and output checkpoint are each byte-canonical JSON followed
by one LF.  The checkpoint schema is
`d972-r07-a0-actual-tau-free-rank-ladder/v3/checkpoint`, and the independently
recomputed binding is
`6f179b061a010bb2a9b427dda6564c7418b18f44da17ea2f28e9e080655326a3`
on both checkpoints.

The exact checkpoint boundaries and canonical internal seals are:

| state | rank / count / cursor round | stored = recomputed `state_sha256` |
|---|---|---|
| input | `111 / 68 / 73` | `3e0d4bc8e2f9a467a0e50ad8435a7360e1953c2baee369225d8aa6fd71379610` |
| output | `143 / 100 / 106` | `35c6d4e8b21b1f72bf4963a7539d14c90ae7cc8bea1a7a10398e462e593b9272` |

The input's complete 68-record accepted list is exact JSON-equal to both the
result prefix and output-checkpoint prefix.  Because all three files are
canonical, the corresponding serialized prefix bytes also agree exactly:
85,174 bytes with SHA-256
`684039158b841d607aa40617778b9267ea96d64a38d952f74e63791b23ea3932`.

There are exactly 32 appended records.  Their canonical list is 40,442 bytes
with SHA-256
`504c5518e3a2ae19ac41d4b2862253a6ec37c3b59ca7f59208fda2c3431ed7fa`.
Their rounds are exactly 74 through 105, hence strictly increasing and all
greater than 73; their transitions are exactly `111 -> 112` through
`142 -> 143`.  Across all 100 records, ranks are the unit chain `43 -> 44`
through `142 -> 143`, rounds are strictly increasing, and the last accepted
round is 105.

All 100 records are corrections with the same exact 20-field shape.  Every
contract integer has JSON integer type; scalars are in `{1,2}`; all required
digests are lowercase 64-hex; every pivot is canonical lowercase 92-hex;
every seed is in `1..44`; all delta letters are in `{1,-1,2,-2}`; and exponent,
coordinate, cursor, fibre-count, target and required-coordinate fields have
the frozen v7-compatible types.  There are exactly 100 distinct pivots, 100
distinct row digests, and 100 distinct canonical source identities
`(kind, seed_index, delta_word)`.

The result and output checkpoint have exact equality of accepted list, count,
rank, round, reason, and current profile.  The result's durable envelope binds
the output checkpoint to exactly 126,377 bytes, SHA-256
`dff9cb181ae40abfac23ccba1b7c819ad353ecbec3825e5922e944dbe4b41b4c`,
count 100 and rank 143.

The final current profile is exactly at physical rank 143, with
`N1=N2=0`, tau coefficients `1:0, 2:0, 3:0`, empty
`unrecognized_keys`, empty `required_coordinates`, and `target_pair=1`.
Its dual and remainder digests are respectively
`dcc4828c1c6ddec817bdad9c2c3f7e2f33db131593e70437e2ca14ac441123e4`
and
`9eed8114d9e3172c7a11153d9c5cd6e5fc2e5184a8d6e3681cce5c82a83b4326`.

## F5. Checker authority, commands, and limitations

The authenticated GHA job executed the exact pinned v7 checker.  Its inherited
chain performs the full independent semantic replay of rows, direct sources,
pivots, pre/post dual and remainder states, rank rises, sealed durable state,
profile, resource boundary, and claims before PASS.  I did not repeat that
large semantic replay locally, as expressly required.  The bounded audit
instead supplied the checks absent from the older checker: exact rank111
68-record byte/JSON prefix equality, exact appended round/rank chain, strict
record typing, and explicit pivot/row/source distinctness.

Representative read-only/bounded commands were:

```powershell
gh api repos/tochiazuma0510-alt/shadow-atelier/actions/runs/33579991982
gh api repos/tochiazuma0510-alt/shadow-atelier/actions/jobs/100092032846
gh api repos/tochiazuma0510-alt/shadow-atelier/actions/artifacts/9831153395
gh api repos/tochiazuma0510-alt/shadow-atelier/actions/runs/33579991982/jobs
gh api repos/tochiazuma0510-alt/shadow-atelier/actions/runs/33579991982/artifacts
gh run view 33579991982 --repo tochiazuma0510-alt/shadow-atelier --job 100092032846 --log
gh api 'repos/tochiazuma0510-alt/shadow-atelier/contents/<pinned-path>?ref=ae74e865ec7ba10d00eca263356afa01d23a2466'
git show 'ae74e865ec7ba10d00eca263356afa01d23a2466:<pinned-path>'
Get-ChildItem -LiteralPath $artifactRoot -Recurse -File | Get-FileHash -Algorithm SHA256
node -e <canonical JSON/seal/prefix/type/chain/terminal auditor> <input> <result> <output>
[System.IO.Compression.ZipFile]::OpenRead($priorZip)
```

The GitHub service digest is the API's digest of its compressed artifact
container; I did not claim to recompute that backend container digest from
the extracted tree.  I did recompute every extracted regular-member hash and
stream-compare every nested prior-ZIP entry.  Bounded command output is
candidate evidence; the authenticated independent producer/checker agreement
makes this finite prefix cross-checked, while `verified=false` remains
unchanged.

No production search, local full semantic replay, workflow dispatch, git or
release mutation, implementation edit, or claim-ledger edit was performed.
The final physical bytes/SHA-256 of this reply are supplied after freeze in
the parent delivery envelope because embedding its own digest would be
self-referential.

GO_FOR_PREFIX_PROMOTION_AND_ARCHIVE
