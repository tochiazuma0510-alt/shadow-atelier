# Luna reply 362 — R07 A4/v6c authority-trace repair

## 1. Binding inputs and verdict

The task198 receipt, acceptance manifest, two attestations, verdict, producer,
checker, and driver were read directly and pinned before implementation.  The
immutable authority identities used by both new owners are:

| owner | bytes | SHA-256 |
|---|---:|---|
| task198 receipt | 31,017,244 | `82f7955580039f2a0271896c928515d26996f636d8e73231331da6a37f6b19f5` |
| task198 acceptance manifest | 2,722 | `cc8c16c8ad8f2d094868f0897bcca2a98adba75c18bf7ff397f0da67fd233ea4` |
| producer attestation | 81 | `b5ab577d14ed490af12e3921ee41cfea533abcbf92d60cc037f0d40035ba5090` |
| checker attestation | 95 | `260eb23f73a8fb6b9cd2316aa4ea6c29a4a6db92e77d8c5c6f4f1dd6e7ff290e` |
| checker verdict | 150 | `ac841c5a979bbe89bdd47c73151ecabf29783793b7b288b4d08c4824596251de` |
| task198 producer source | 137,169 | `6b2645b80f97256a659af81e856c086cca724b36e2a22ae70335b29ffa95d44c` |
| task198 checker source | 157,253 | `001277d44dbbc2acd7e03c6ecb6c6419df84996ae188cbb4be7b18f7cfb56ca1` |
| task198 GHA driver | 20,541 | `6048174be12d5f6f48508f1b2e80c87b3e1cb9df9ed348b30b6d3e19420b5068` |

Task360's v6b result was `REJECT / UNEXECUTED`; all defects in its Sections
2–7 were treated as binding.  No candidate code, Python, Node, GAP, GHA,
workflow, network, or git command was run.

## 2. Sole v3 outputs and scope

Only the four commissioned outputs are present:

| output | bytes | SHA-256 |
|---|---:|---|
| `search/d972_r07_a4_actual_owner_trace_producer_v3.py` | 94,299 | `22edde4e3c2fa00ad858f7aa8175774037c0f02ebd28eec27d83ffd184bb534c` |
| `crosscheck/check_d972_r07_a4_actual_owner_trace_checker_v3.py` | 91,766 | `f9b1305d975a53309fff527aa9061aa3182fb3409a7e4003d35044cb98e64c25` |
| `search/certs/d972_r07_a4_actual_owner_trace_authority_fixture_v3_20260829.json` | 8,457 | `0d58bace814a7b838f7bf08a91ca7e1eea79e7d4d5099b52281ea7cce61ed225` |

The fixture canonical body self seal is
`faa301467e8c5047b192da539467409631cdd9abe5a480f18aa175926b897a14`.
The fixture is acyclic: it pins external task198 authorities and the row/cap
contract, but neither v3 program nor this reply.  Both programs are stdlib
only; the checker has no producer import or shared helper.

The registered scope is `covered_rows=[1,2,3,4,5,6,7]`,
`remaining_rows=[8,...,48]`, `candidate_only=true`, `synthetic=false`,
`full_a4_selftest=false`, and `actual_a4_numerator=false`.

## 3. Semantic receipt/manifest reseal DAG

Producer seal/route code is at lines 413–436 and 540–562; checker code is at
lines 274–296 and 376–390.  Receipt sealing removes only
`self_digest_sha256` and rejects a foreign top-level
`manifest_self_digest_sha256`.  Manifest sealing removes only
`manifest_self_digest_sha256` and rejects a foreign receipt seal.

`SealedReceipt` and `SealedManifest` explicitly carry DOM, canonical raw,
raw SHA, byte length, and the new self seal (producer lines 140–155; checker
lines 86–91).  `copy_manifest` checks that tuple and binds all three receipt
values from it (producer line 576; checker line 399).

Rows 1/5/6/7 use the complete five-node DAG, constructed in producer
`_plan` lines 626–650 and checker `make_plan` lines 437–461:

```text
changed receipt body
 -> new receipt self seal
 -> new receipt raw SHA and byte length
 -> changed manifest nested receipt binding
 -> new manifest self seal/raw SHA
```

Row 2 reseals only the changed manifest.  Rows 3 and 4 intentionally perform
no downstream reseal.

## 4. Exact task198 type and ABI validation

Producer's fused typed row walk is lines 438–470 and its presentation checks
are lines 471–483.  Checker equivalents are lines 297–327 and 328–339.
They enforce exact key sets, exact strings, exact positive integer fields,
orientation in `{-1,1}`, layer-local ordinals, all seven chunk seals and
coverage, `sealed=true`, `prefix_complete=true`, resume cursor, source
encoding, legacy digest, stored row digest, and the retained empty Cayley
word in the same traversal.  `strict_equal` rejects bool/float/integer
substitution in layer counts.

The full authenticated task198 evaluator canary object is independently
frozen in producer line 114 and checker line 79.  The field checks and the
final `strict_equal(canaries, ABI_CANARIES)` checks are at producer lines
507–523 and checker lines 352–366.  They cover exact module, row digest,
coordinate widths/ledger, entry points, encoding, semantics, all eight
canary keys, exact words, IDs, and every exact nested value blob.  Mutation
comparisons additionally use the authenticated baseline evaluator object.
The 11-field occurrence ledger, its canonical digest, typed coordinate-owner
ledger/digest, and exact normal-generation object remain independently
reconstructed in producer lines 484–506 and checker lines 340–351.

## 5. Physical owners, baseline lifetime, and row 4

The no-follow parent walk and physical owner reads are producer lines 266–381
and checker lines 151–247.  Every pinned source, fixture, manifest, and
receipt retains its live fd for the invocation.  Before and after each case,
`revalidate_all` rewinds and hashes the retained fd at exact length, checks
device/inode/type/mode/size/link count/`mtime_ns`, and compares the registered
pathname through a no-follow parent walk.  `baseline_revalidated` is recorded
only after that transcript succeeds.  Invocation-level `finally` blocks close
all retained fds.

Row 4 creates an invocation-unique temporary parent outside the workspace and
repository, asserts the exact outside receipt path is absent, routes that path
through the registered containment gate before any basename shortcut, and
checks both outside owner path and parent absence during disposal.  Its
`owner_disposed` value is derived from that actual outside path, never a shared
sibling.

The supported boundary is POSIX with `O_NOFOLLOW`, `O_DIRECTORY`, `dir_fd`,
no-follow `stat`, and directory fsync support.  Windows and unsupported
primitives are typed input stops; no Windows PASS is claimed.

## 6. Meter ownership and final resource formulas

One meter/counter spans fixture authentication, the baseline, all seven cases,
and optional publication.  Allocation/copy reservations are made before use;
exceptional clone/copy paths release their own reservations.  Case `finally`
blocks release clone, receipt, manifest, canonical, wire, and workspace cache
owners before the next case.

With `S=315,289` (six source pins), `F=8,457`, `R=31,017,244`, and `M=2,722`,
the source formulas at producer lines 89–98 and checker lines 58–67 are:

```text
opened    = S+F+R+M + 3(R+M) + (R+8+M) + (M+1) + R
          = 186,443,551
temporary = 3(R+M) + (R+8+M) + (M+1) + R
          = 155,099,839
parsed    = F + 4(R+M) + (R+8+M) + (M+1) + M + M
          = 155,116,462
baseline peak = 2S + 8F + 8M + 8R
              = 248,857,962
largest peak  = baseline peak + 2(R+8+M) + 6(R+8+M)
                + 200,000,000 + 10,000 + (R+8)
              = 728,045,006 < 750,000,000
DOM charged   = opened + parsed + 4*200,000,000 + 4*10,000
                + 10,000 + R
              = 1,172,627,257 < 1,500,000,000
```

The corrected deltas include row 2's `+1`, row 6's `+8`, each 10,000-byte
changed-manifest clone, canonical transients, retained baseline handles, and
all four semantic receipt/manifest rewrites.  The seven-case account is
`METERED_LOGICAL_OPENS=19+20+14=53`, `INTENDED_WRITES=10`, and
`INTENDED_EVENTS=16+50=66`; directory-component opens and retained-fd
revalidation reads are separately identified and are not misreported as the
full physical-operation count.

Optional output is separately guarded: its canonical bound is 35,000,000
bytes, its temporary reservation is the actual final raw length, and it adds
one publication write and five logical file/parent opens.  It runs only after
case owners and the fixture are released, so it is not silently merged into
the seven-case peak claim.  No optional output was executed.

## 7. Bound-parent, failure-atomic optional publication

Producer output code is lines 740–837; checker output code is lines 527–621.
Both retain one no-follow parent fd, use only dir-fd-relative operations,
reject stale targets, stage with exclusive creation, fsync staged bytes,
verify exact regular-file bytes/SHA, publish with exclusive hard-link, unlink
the staging link, fsync the staging directory and parent, verify through the
same parent fd, and compare parent identity.  Any post-publication failure
rolls back the final name through that fd, fsyncs rollback, asserts absence,
and propagates a typed failure.  All parent, stage, write, and verify fds are
closed under `finally`.

## 8. Rows 1–7 and independent checker

Producer `run_mutation` is line 687 and checker `run_case` is line 488.  The
constructor supplies the observed physical owner, kind, and logical path;
evidence is not authored by a name-indexed acceptance table.  Each route has
one narrow expected terminal, one terminal count, owner identity change,
baseline transcript, resource before/after snapshot, disposal proof, and the
complete reseal DAG where applicable.

| row | actual owner and mutation | producer first gate | checker first gate | downstream reseal |
|---:|---|---|---|---|
| 1 | receipt `Delta0.presentation.rows[0].ordinal` | `producer.authority.row_order` / `producer:authority:layer_ordinal` | `checker.authority.row_order` / `checker:authority:layer_ordinal` | five-node receipt→manifest DAG |
| 2 | manifest `accepted` | `producer.authority.manifest_acceptance` / `producer:authority:manifest_acceptance` | `checker.authority.manifest_acceptance` / `checker:authority:manifest_acceptance` | manifest self only |
| 3 | receipt raw bytes | `producer.transport.receipt_identity` / `producer:transport:receipt_sha256` | `checker.transport.receipt_identity` / `checker:transport:receipt_sha256` | none |
| 4 | invocation-unique outside receipt path | `producer.transport.path_containment` / `producer:path:registered_containment` | `checker.transport.path_containment` / `checker:path:registered_containment` | none |
| 5 | normal-generation proof | `producer.authority.normal_generation` / `producer:authority:normal_generation_proof` | `checker.authority.normal_generation` / `checker:authority:normal_generation_proof` | five-node receipt→manifest DAG |
| 6 | bridge occurrence ledger | `producer.authority.bridge_occurrence` / `producer:authority:bridge_occurrence_ledger` | `checker.authority.bridge_occurrence` / `checker:authority:bridge_occurrence_ledger` | five-node receipt→manifest DAG |
| 7 | evaluator coordinate ABI width | `producer.authority.evaluator_abi` / `producer:authority:evaluator_abi_canary` | `checker.authority.evaluator_abi` / `checker:authority:evaluator_abi_canary` | five-node receipt→manifest DAG |

Both result scopes retain rows 8–48 as uncovered and retain
`actual_a4_numerator=false`; no lift/fake/Ihara or numerator logic was added.

## 9. Freeze and remaining limitations

The three machine owners and fixture self seal above are frozen from read-only
PowerShell/hash inspection.  Static implementation is complete for the
finite rows-1–7 authority trace.  Runtime execution, GHA, measured RSS/wall
time, the full 48×2 self-test, rows 8–48, A4 completion, lift, fake, Ihara,
and any mathematical numerator remain intentionally absent.

TASK360 SEMANTIC RESEAL DEFECTS:       REPAIRED
TASK360 DOM OWNER / PEAK DEFECT:       REPAIRED
TASK360 BASELINE REVALIDATION:         REPAIRED
TASK360 EXACT TYPE / ABI VALIDATOR:    REPAIRED
TASK360 OUTPUT ATOMICITY / DURABILITY: REPAIRED
ROWS 1--7 PRODUCER/CHECKER ROUTE:      IMPLEMENTED
EXECUTION / GHA:                       UNEXECUTED
FULL 48x2 SELFTEST:                    INCOMPLETE
ACTUAL A4:                             remains 1/3
LIFT / FAKE / IHARA:                   NONE

TASK362_R07_A4_V6C_AUTHORITY_TRACE_REPAIR
