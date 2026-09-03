# Sol(max) Task702: Task699 P1 structural-ingest audit

## Verdict

`verified=false`

The frozen actual artifacts and the successful lead census are internally
consistent, but the Task699 producer does **not** yet pass its complete
contract.  Two finite code/fixture defects and one required receipt omission
remain.  I did not repeat the 1.7-GiB-RSS all-five JSON replay and did not
perform any production, workflow, GHA, git, or code change.

## Audited inputs

| path | bytes | LF lines | SHA-256 |
|---|---:|---:|---|
| `search/d972_r07_grade2_specific_owner_prejoin_v1.py` | `46339` | `523` | `72bf135cd86f96ffb050e9033c2fe3d40942ae55a900c5310c10781fab3c0cb2` |
| `sol/sol_task_702_audit_r07_task699_p1_structural_ingest.md` | `1633` | `31` | `e999063017cd7f9d44d1937dd23cb0d928bcd9036eeab8beab46ab63080d7e71` |
| `sol/luna_task_699_r07_p1_four_block_structural_ingest.md` | `4231` | `79` | `483c75985cbd8b26fd7e26db3fe598a0e4feff7ddffdf3ed25809cc70fce408a` |
| `sol/luna_reply_699_r07_p1_four_block_structural_ingest.md` | `2865` | `56` | `a08d6407d80305323559ec7a89e9cf1ba4b2ed839f552ecdee55a49c1954d9f4` |
| `sol/proof_r07_grade2_lazy_presentation_interface_v480.md` | `7981` | `228` | `46b917a2e353951b0a345f3469c1e145408f31d0a53933241b2cf9ef438ddcea` |
| `sol/proof_r07_grade2_p1_disjoint_lead_completion_v481.md` | `4548` | `123` | `462b74a314ed29fcb028910a02a0c9bf4bf3daeb481657448a21981ec390f9c4` |
| Task647 launch contract | `37363` | `740` | `def1be12d5c8337daf82c1f25427c936b2d5d55875cd27109d9487189c4e5cfb` |
| accepted Task691 audit | `5029` | `109` | `50b5bb9ee4b08b5fb92635467a8ae8d833d2fea61bbdb118f0352dcd235e9a27` |
| accepted Task698 re-audit | `5729` | `117` | `951505daa61611a958ed355e76d9c0161911248383d05b202a3388b74fb659dc` |

Every listed input has a final LF.

## Passing frozen-artifact and lead checks

Static inspection confirms that the production all-five path calls, in order,
`ingest_prepare(..., retain=True)`, `validate_block_envelope`,
`validate_block_semantics`, and `scan_block_basis` for each of exactly four
ordered CLI roots.  The block envelope uses the fixed indexed body pin and an
exact three-file roster.  Its semantic pass checks the fixed prepare parent,
character/index, packet, rank, attempts, FIFO, actor order, and all declared
origin/actor/DAG expressions; `validate_expression(..., earlier_than=pivot)`
rejects self and forward DAG reductions.  Each origin has the charged exact
key set and range/letter predicate, and the canonical digest is recomputed
from the complete DAG node list.

The basis consumer first applies the typed receipt gate and then, in the very
pass that derives each lead, rereads exactly 4,536 bytes per row, applies the
full `0..80` byte gate, updates count and SHA-256, compares the declared lead,
requires coefficient one, checks EOF, and compares before/after size,
`mtime_ns`, and file identity.  Thus the prior Task698 same-consuming-pass
repair is preserved for both old and new rows.

Without parsing the four large bodies, I independently streamed their pinned
hashes and scanned the compact basis blobs.  The exact receipts are:

| block | rank | HEAD SHA-256 | body bytes / SHA-256 | basis bytes / SHA-256 | local-lead SHA-256 | local range |
|---:|---:|---|---|---|---|---|
| 0 | 1509 | `54a8147e9ea1b61340d31818ccbc8e51b7d5b7150b71cfe5b6b8676e68f72fca` | `74883943` / `9ebcc7ad1141c20aeaff82eb4a83a9489dc492b30220547f23526b4fcdd8dc74` | `6844824` / `cc7e38114afc58e3aba10fa340a6ebd4f9a7a4752d5bb5fb9408ea8d84021e39` | `fb35de7583bc72ba21a21381e0acf45e1196ff31bab6a325806e4a005675d1f2` | `0..2444` |
| 1 | 1512 | `bc98ffd9642602bde075849f964fd36c30c1a7c1939a274228b392d17f0f9f92` | `75400514` / `d783bbe6c92c15a241eb78d0b25bca5e7c00f60799ce82f6df8b1d3ee7a202f6` | `6858432` / `0223f72b7d2cb8a72f2ff99b8812fea977ed761c8505dab52ad3fba284b93461` | `ed578063d507de2f83a75839e692ba9fdb194d46b8fcdeef16531fc8615234b0` | `0..2948` |
| 2 | 1512 | `d93654eb7c3983fb6cc6498e4c9c35b05ad01633b934fe2710c82aa8b70767b4` | `75340879` / `a6dcc904fc3e9daae008f72de7e83ffadcd39055d557621b9cdf06baea0e83ac` | `6858432` / `602f23081aa609973860eac24d2f65104a9530c8ddf356d60a9d0378921b99f6` | `ecf98d8170660028ddc5e12f01fcf84576c5772bdc6e19889e278652b849c1b7` | `0..2444` |
| 3 | 1512 | `36712a93ea23435abcebf81b1c574d12c630694aeff236b2378c338f5a00d5e2` | `75407216` / `642a4ec0ad6ad4ea659e84330e34006c767ca029203446cb64a17c151fefdb01` | `6858432` / `4ed4de15c00290f60e5fd2d57dd94db3103be92c602d92481f2835d9d96db0b9` | `d560e155db99283dafa8068537bc389248f6af66235478fd421bb09919e9dd57` | `0..2948` |

All 6,045 scanned rows matched the pinned body's declared lead, had
coefficient one, and were distinct within their block.  A bounded independent
pass over only the 67,011,332 compact old/new basis bytes reproduced the exact
old census and shared-summary result:

```text
old rows / distinct / coefficient-one  2014 / 2014 / 2014
old lead+coefficient SHA-256            1be9a7a806fbb70f5d9825d865004b049d8c0d092a840a0c31ce951b4d5976ee
offsets                                 [0,505,1008,1511,2014,3523,5035,6547,8059]
all rows / distinct / coefficient-one  8059 / 8059 / 8059
all lead+coefficient SHA-256            508db9f3dd63a7a8db22e9e10604af6c0660179ce60e9f9919391e86d0cf80e9
coefficient-one row/lead SHA-256        dafd43d5795c88c1324ea5b104633f423f886b583a7e14877424961880402d59
all local-lead SHA-256                  eb6e16ae954c0d64e8af1c4b144aaa172491ab51948184f5119143c6928823a7
empty collision-list SHA-256            37517e5f3dc66819f61f5a7bb8ace1921282415f10551d2defa5c3eb0985b570
```

The mapping `24192 + 18144*a + q` places the new rows in the four mutually
disjoint v481 degree-one intervals; Task693/698's old rows occupy only degree
zero or the final auxiliary interval.  The one shared production summarizer
therefore correctly detects any actual cross-family collision and yields rank
8,059 on these bytes.

The serial loop retains the prepare object, one parsed large block object, a
compact lead-descriptor list, and one packed row at a time.  It deletes each
block body after extracting diagnostics.  It constructs no dense family,
does no Task640 join, precision-two work, or semantic `44+4*8059` equality
replay, and its terminal explicitly reports all three as false.  The bounded
selftest still exits zero, but that does not cover the blockers below.

## F702-1: block semantic typing is incomplete

In the frozen `validate_block_semantics` DAG-node predicate, the declared
`pivot_leads[pivot]` is checked with `_plain_int`, but the duplicated
`node['lead']` field is only compared by Python equality.  Consequently a
node with `lead=False` and declared lead `0` is accepted, because
`False == 0`; recomputing the canonical DAG digest does not close the hole.  A
bounded mutation through the exact production semantic helper confirmed
`node_lead_bool: ACCEPT`.

The same predicate compares `downstream_claim_flags` to `FALSE_CLAIMS` by
ordinary dict equality.  Replacing every required JSON boolean `false` by the
integer `0` is likewise accepted; the production-helper probe reported
`false_claim_ints: ACCEPT`.  This is the charged lead/plain-type and exact
false-claim surface, not generic hardening.  The current pinned bodies contain
the intended values, so this defect does not alter the actual census above.

Minimal repair: require `_plain_int(node.get('lead'))` before equality, and
require the exact downstream key set with every value `is False`.  Add both
mutations to the live block-semantic fixture and require rejection.

## F702-2: no fixture reaches the production block-envelope helper

Task699 required the bounded fixtures to exercise the live **block** envelope
helper.  They do not.  `block_fixture` calls `validate_block_semantics`,
`analyze_block_row`, and `summarize_old_leads` directly; the existing
`envelope_fixture` calls only `validate_prepare_envelope`.  Thus none of the
reported block mutations enters `validate_block_envelope`, and the claim that
the live block-envelope fixture was exercised is unsupported.  The existing
wrong-parent case mutates the block body and reaches the semantic parent gate;
it does not test the canonical block HEAD/three-file-roster path.

Minimal repair: make one bounded, self-contained three-file block root enter
the same block-envelope helper used by `ingest_all_five`, then send at least
the charged wrong-parent envelope mutation through it.  A fixture-only digest
parameter analogous to the already accepted prepare-envelope pattern, or a
factored common byte validator, is sufficient; production must retain the
fixed `PARENTS` pin.

## F702-3: Task699's real replay lacks its required code-byte receipt

Task699 explicitly required its reply to report exact candidate file bytes,
LF count, and SHA-256.  The reply reports artifact sizes/digests and the real
terminal, but omits all three candidate values.  This audit measures the
current file as `46339` bytes, `523` LF lines, SHA-256
`72bf135cd86f96ffb050e9033c2fe3d40942ae55a900c5310c10781fab3c0cb2`,
with a final LF; that observation cannot retroactively bind the claimed
1.7-GiB replay to those exact bytes from the Task699 reply alone.

After F702-1 and F702-2 are repaired, the replacement serial run/reply must
state the new exact code receipt together with its terminal and actual
counters.  The independent checker and semantic equality replay remain
separate later gates and are not requested by this repair.

`FAIL_P1_STRUCTURAL_PRODUCER`
