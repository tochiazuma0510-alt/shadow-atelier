# Luna reply 358 — A4/v6b rows 1--7 authority-trace finite repair

実装は指定された4ファイルだけに限定した。候補コード、Python/Node/GAP、GHA、
workflow、git、network は実行していない。本 reply の runtime/RSS 欄は
`UNEXECUTED` であり、静的な source inspection と read-only hash inspection のみである。

## Machine identities

| file | bytes | SHA-256 |
|---|---:|---|
| `search/d972_r07_a4_actual_owner_trace_producer_v2.py` | 66,200 | `ca8755b6ad4bf9de001783d76d4de0e4d5d8680795540264ee843680a8deb3e9` |
| `crosscheck/check_d972_r07_a4_actual_owner_trace_checker_v2.py` | 62,039 | `8ec2fb33d17ac19cab2f13a141e91f05423b87e9edb82fbd8f5543512c0d3252` |
| `search/certs/d972_r07_a4_actual_owner_trace_authority_fixture_v2_20260829.json` | 8,457 | `8fd4de7b89eb07e3adb272782f3052c9b9b3bb90bf7a27212933ae40f892a91d` |

The fixture top-level canonical self seal is
`abd50579d5d18857ea015bc07fcef4b3bdc7f8f145cfe555f0146f746700d88f`.
The fixture is `candidate_only=true`, `synthetic=false`, `covered_rows=[1..7]`,
`remaining_rows=[8..48]`, and `full_a4_selftest=false`.

## Source, authority, and import graph

The producer and checker are separate stdlib-only implementations. They do not
import one another, task356/v1, task357/v1, or task198 code. The producer uses
`PhysicalStore`; the checker independently uses `AuthenticatedOwner`. Both pin
the same lexical v2 fixture, its 8,457-byte SHA above, and its canonical self
seal. The fixture does not pin either v2 program, so the graph is acyclic.

Both sides physically open and pin the task198 receipt
(`31,017,244` bytes, SHA
`82f7955580039f2a0271896c928515d26996f636d8e73231331da6a37f6b19f5`, receipt
self `c8f7e65f6ec7553ab31928c911575de45fc0e3d70cd6e1d678bbebfee7502b9f`), the
acceptance manifest (`2,722` bytes, SHA
`cc8c16c8ad8f2d094868f0897bcca2a98adba75c18bf7ff397f0da67fd233ea4`, manifest
self `0f630669a906c93a3b7d40bd36633213316ff8da1b46ca254a552b3636963684`),
both attestations, checker verdict, and the three task198 source/driver pins.
The producer pin table is at lines 74--81; the checker pin table is in
`authenticate` at line 378. The manifest graph is independently reproduced in
producer lines 401--424 and checker lines 302--315, including artifact, run,
head, member, terminal, source, attestation, verdict, and nested receipt seal.

Receipt and manifest use distinct codecs. Producer `seal_receipt`/`seal_manifest`
are lines 520--543 and checker counterparts are lines 388--406. Receipt removes
and inserts only `self_digest_sha256`; manifest removes and inserts only
`manifest_self_digest_sha256`, rejecting a foreign top-level receipt seal.
`parse_object` performs exact sorted compact ASCII raw comparison (producer
359--389, checker 260--287), while the fixture is intentionally parsed as the
pinned fixture format and checked by its own self digest.

## Physical route and row traces

The single ordinary route admits both paths before semantic manifest binding:
producer `admit_path`/`ordinary_route` lines 343--357 and 490--504; checker
`admit`/`ordinary` lines 250--258 and 368--375. Candidate paths are lexical;
candidate `.resolve()` is not used. POSIX directory and final-component
`O_NOFOLLOW` traversal plus one-handle before/read/after identity are producer
lines 233--341 and checker lines 149--248. Windows and a platform without the
registered no-follow API terminate as typed unsupported input, never PASS.

Every mutation enters its ordinary route exactly once, catches only the narrow
trace exception, and leaves `MutationAccepted` outside that catch: producer
`run_mutation` lines 626--674 and checker `run_case` lines 481--518. The
fixture's producer and checker first-rejection maps are independently checked
after the ordinary event has fired; the observed owner must differ from the
baseline owner (including path, mode, nlink, bytes and fd-derived identity),
`terminal_count` must be exactly one, and the ordinary validator must occur once.
The evidence projection contains no raw device/inode/mtime/temp-path values.

| row | actual owner mutation and physical constructor | producer ordinary entry → exact first rejection | checker ordinary entry → exact first rejection | downstream reseal |
|---:|---|---|---|---|
| 1 | `authority.receipt.Delta0.presentation.rows[0].ordinal`; one receipt DOM clone and physical receipt file | `producer.authority.row_order` → `producer:authority:layer_ordinal` | `checker.authority.row_order` → `checker:authority:layer_ordinal` | receipt self; manifest receipt binding; manifest self |
| 2 | `authority.manifest.accepted`; one manifest clone and physical manifest file | `producer.authority.manifest_acceptance` → `producer:authority:manifest_acceptance` | `checker.authority.manifest_acceptance` → `checker:authority:manifest_acceptance` | manifest self only |
| 3 | `authority.receipt.raw_bytes`; one physical bytearray with changed final byte | `producer.transport.receipt_identity` → `producer:transport:receipt_sha256` | `checker.transport.receipt_identity` → `checker:transport:receipt_sha256` | none |
| 4 | `authority.receipt.path`; lexical workspace-parent path, no basename hook | `producer.transport.path_containment` → `producer:path:registered_containment` | `checker.transport.path_containment` → `checker:path:registered_containment` | none |
| 5 | `authority.receipt.Delta0.presentation.normal_generation_proof.Gamma_cayley_edge_count`; receipt clone/file | `producer.authority.normal_generation` → `producer:authority:normal_generation_proof` | `checker.authority.normal_generation` → `checker:authority:normal_generation_proof` | receipt self; manifest receipt binding; manifest self |
| 6 | `authority.receipt.bridge.occurrence_ledger[0].block`; receipt clone/file | `producer.authority.bridge_occurrence` → `producer:authority:bridge_occurrence_ledger` | `checker.authority.bridge_occurrence` → `checker:authority:bridge_occurrence_ledger` | receipt self; manifest receipt binding; manifest self |
| 7 | `authority.receipt.evaluator.coordinate_widths[0]`; receipt clone/file | `producer.authority.evaluator_abi` → `producer:authority:evaluator_abi_canary` | `checker.authority.evaluator_abi` → `checker:authority:evaluator_abi_canary` | receipt self; manifest receipt binding; manifest self |

The owner constructors are producer `_mutate_receipt` lines 600--604 and
`run_mutation` lines 624--654; checker `_mutate` lines 462--466 and `run_case`
lines 479--505. The seven local cases use independent workspaces, remove the
hard-link probe before the next case, evict exact workspace cache keys, remove
the workspace, and recheck both unchanged baseline identities before setting
`baseline_revalidated=true` (producer 655--673; checker 505--517).

## Exact manifest reseal DAG

For rows 1, 5, 6, and 7 the changed receipt body is serialized once and hashed
to the receipt's `self_digest_sha256`. The changed manifest then binds the
receipt basename, bytes, receipt SHA, and receipt self seal; its body is
serialized once and hashed to `manifest_self_digest_sha256`. The final output
serialization is the manifest leaf. Row 2 changes only `accepted`, then seals
the manifest with `manifest_self_digest_sha256`; it does not forge a receipt
seal. Rows 3 and 4 are transport/path owners and perform no downstream reseal.
`seal_receipt` and `seal_manifest` retain returned final bytes through their
atomic consumer; body bytes are explicitly dead before the final serialization.

## Meter, I/O, peak lifetime, and cache proof

There is one meter from fixture authentication through baseline, seven cases,
and optional output. Producer and checker caps are identical:

`opened_bytes=250,000,000`, `temporary_bytes=250,000,000`,
`canonical_bytes=750,000,000`, `dom_bytes=1,500,000,000`,
`peak_live_bytes=750,000,000`, `opens=256`, `writes=256`, `events=10,000`,
`mutations=7`.

All large bytearray, DOM, clone, canonical, file and open reservations happen
before allocation/use. Unique opened input bytes are bounded by

`315,289 (six task198 source pins) + 31,017,244 + 2,722 + 8,457`
`+ 2,722 (row 2 local manifest) + 31,017,244 (row 3 local receipt)`
`+ 4*(31,017,244 + 2,722) (rows 1,5,6,7 local receipt+manifest)`
`= 186,443,542 < 250,000,000`.

The corresponding required mutation temporary-write bytes are at most
`2,722 + 31,017,244 + 4*(31,017,244 + 2,722) = 155,099,830`; the optional
receipt output has a separate 35,000,000-byte canonical bound, remaining below
the temporary cap. Actual canonical and DOM work is charged to their larger
caps above.

The retained peak calculation is explicit and uses named owner lifetimes:

```text
baseline cache/wire       = 2*(31,017,244 + 2,722 + 8,457 + 315,289)
                          = 62,687,424
baseline parsed DOM       = 6*(31,017,244 + 2,722 + 8,457)
                          = 186,170,538
one case cache/wire       = 2*(31,017,244 + 2,722)
                          = 62,039,932
one case parsed DOM       = 6*(31,017,244 + 2,722)
                          = 186,119,796
one semantic receipt clone (preallocation bound) = 200,000,000
receipt parse canonical transient bound           = 31,017,244
P_peak <= 62,687,424 + 186,170,538 + 62,039,932
          + 186,119,796 + 200,000,000 + 31,017,244
        = 728,034,934 < 750,000,000.
```

The seal phase is lower: its final receipt raw is retained with a 35,000,000
bound through `atomic_write`, while the body raw is deleted before final
serialization; the manifest clone/final raw are retained until their atomic
write. For a semantic row, the receipt final raw is held through
`copy_manifest`, then `del raw` precedes `release_retained(receipt_owner)`;
the clone and manifest clone remain live through ordinary validation and are
released in the case `finally`. Canonical-input `raw` is similarly deleted
before its wire token is released. Baseline parsed DOM owners remain live until
the end of `execute`; the fixture owner remains live until `main` has returned
from `execute` (and is deleted before optional output). Output raw is deleted
before its output token is released. Thus the formula counts the simultaneous
baseline cache + baseline DOM + case cache + case DOM + clone + parse canonical
owners, while body/final raw tokens follow actual references rather than a
post-hoc peak claim.

The store cache is keyed by exact absolute lexical path. `evict_workspace`
deletes every key satisfying the common-path containment predicate and releases
that key's `cache:<path>` token; it then asserts no key remains under the
workspace. `close` releases any remaining immutable source/baseline tokens.
There is no platform-specific `Temp` substring, no retained five-mutant raw
roster, and no second baseline 31-MB read: registered paths hit the same cache
entry. Canonical seal paths are body serialization → one hash → final
serialization, and all exception paths release only their own reservation.

## Remaining limitations

This is the finite rows 1--7 authority-trace tranche only. Rows 8--48, the full
48x2 selftest, algebra/DAG merge, lift, fake, Ihara, and any A4 completion are
not implemented or claimed. Runtime execution, GHA, measured wall time, and
measured RSS are intentionally absent. Windows is a typed unsupported-input
route in this tranche; no Windows PASS is claimed. Optional output is guarded
by stale-target rejection, containment, exclusive staged linking, parent
identity checks, and file/directory fsync, but no output run was performed.

TASK357 NINE-ITEM REPAIR:          IMPLEMENTED
ACTUAL BASELINE ROUTE:             STATICALLY REACHABLE
ROWS 1--7 PRODUCER TRACE:          IMPLEMENTED
ROWS 1--7 CHECKER TRACE:           IMPLEMENTED
V297/V298 PHYSICAL SUBSTRATE:      IMPLEMENTED
STATIC CAPS / PERFORMANCE:         IMPLEMENTED
EXECUTION / GHA:                   UNEXECUTED
FULL 48x2 SELFTEST:                INCOMPLETE
SOL(MAX) REAUDIT REQUIRED:         YES
ACTUAL A4:                         remains 1/3
LIFT / FAKE / IHARA:               NONE
TASK358_R07_A4_V6B_AUTHORITY_TRACE_FINITE_REPAIR
