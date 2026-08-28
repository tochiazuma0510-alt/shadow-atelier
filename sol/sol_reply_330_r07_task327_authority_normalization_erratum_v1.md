# Sol(max) reply 330 — task327 authority normalization erratum

## Verdict

**PASS / UNEXECUTED.**  Task330 replaces the sole false expected reference
in task327.  With that commissioned correction, the exact cross-capture
normalization passes and reply327 contains no further authority-bundle
blocker.  Every other independently audited task327 gate is retained without
change.

This is an authority-input ruling only.  It neither changes nor authorizes
the rejected A4/v2 consumer, SELFTEST, production, actual local evaluator,
closure, K/anchor, lift, fake, or Ihara work.

Only read-only PowerShell byte/hash inspection was used.  Python, Node, GAP,
GHA, workflows, network, git, producer, and checker were not run.  No
manifest, receipt, attestation, or verdict byte was changed.

## 1. Corrected cross-capture comparison

The preserved producer-only capture is available.  From both it and the
direct-run receipt I removed exactly the two top-level members `resource` and
`self_digest_sha256`, then hashed and compared the complete remaining
canonical objects while retaining the full top-level `resume` member.

```text
                                      direct                  producer capture
resume retained                       true                    true
normalized bytes                      31,016,535              31,016,535
normalized SHA-256                    8d6b9a7ed7d7ffaf61962678cd0e8bb3f4e6a219728c44cd1509e6c2cf2698ba
exact byte equality                   true
```

Thus the corrected task330 requirement passes exactly:

```text
bytes  = 31,016,535
sha256 = 8d6b9a7ed7d7ffaf61962678cd0e8bb3f4e6a219728c44cd1509e6c2cf2698ba
```

The old 30,582,643-byte / `595dbe85...` reference is superseded.  As proved
in reply327, it arose only when `resume` was removed too; it is not used in
this ruling.

## 2. Retained task327 audit ledger

The corrected bundle remains the same five files.  Their identities were
read back again and are unchanged:

| member | bytes | SHA-256 | inherited gate |
|---|---:|---|---|
| receipt | 31,017,244 | `82f7955580039f2a0271896c928515d26996f636d8e73231331da6a37f6b19f5` | PASS |
| acceptance_v2 manifest | 2,722 | `cc8c16c8ad8f2d094868f0897bcca2a98adba75c18bf7ff397f0da67fd233ea4` | PASS |
| producer attestation | 81 | `b5ab577d14ed490af12e3921ee41cfea533abcbf92d60cc037f0d40035ba5090` | PASS |
| checker attestation | 95 | `260eb23f73a8fb6b9cd2316aa4ea6c29a4a6db92e77d8c5c6f4f1dd6e7ff290e` | PASS |
| checker verdict | 150 | `ac841c5a979bbe89bdd47c73151ecabf29783793b7b288b4d08c4824596251de` | PASS |

The following complete inheritance ledger records every task327 gate rather
than treating its prior REJECT as an unexamined premise:

- **Canonical bytes and seals — PASS.**  Receipt, new manifest, and verdict
  are compact ASCII canonical JSON with zero CR/LF; attestations are their
  exact one-LF terminal lines.  Receipt self digest
  `c8f7e65f6ec7553ab31928c911575de45fc0e3d70cd6e1d678bbebfee7502b9f`
  and manifest self digest
  `0f630669a906c93a3b7d40bd36633213316ff8da1b46ca254a552b3636963684`
  independently recompute after removal of only their designated seal field.
- **Direct-run authority — PASS.**  The manifest binds
  `accepted=true`, `independent=true`, `synthetic=false`, direct run
  `33155710862`, head
  `bed1d5e6b41477b8799f2a33a24e46f7800f9510`, artifact `9686477718`,
  archive digest
  `8e1d218cb3d0e09e7a633d2c7d4481f232b33e76eaafc51223c307a2c62e0854`,
  and the exact receipt member on both producer and checker sides.  No
  producer-only capture id is substituted.
- **Attestations and independent verdict — PASS.**  Both terminal basenames,
  bytes, and hashes are bound.  The complete canonical checker verdict has
  the exact crosscheck/v2 schema, `accepted=true`, `independent=true`, and
  receipt terminal `ROOF_BRIDGE_ISOMORPHISM`; its full semantic object equals
  the manifest binding.
- **Current task198 sources — PASS.**  Producer, checker, and driver remain
  exactly `137169/6b2645b8...`, `157253/001277d4...`, and
  `20541/6048174b...`, respectively, with their exact bound paths and full
  SHA-256 values recorded in reply327.
- **Receipt envelope and roster — PASS.**  Schema/status/terminal are the
  accepted values.  All 6,441 rows scan without mismatch in the exact local
  blocks `Gamma_Cayley 1..6318`, `action 1..104`, and `Q0_lift 1..19`.
  The independently recomputed row digest is
  `e00880c01bc96ba8f0549311f4955662668d74001ecf5c06097646dad4268950`.
- **Seven chunks — PASS.**  The exact intervals `[0,1024)`, `[1024,2048)`,
  `[2048,3072)`, `[3072,4096)`, `[4096,5120)`, `[5120,6144)`, and
  `[6144,6441)` are sealed and prefix-complete; every slice hash recomputes.
  Their canonical ledger digest remains
  `8632f613886b4e2f70fc0b49dff0274122590ff3970a16d689c0d3c4507496aa`.
- **Normal generation — PASS.**  The independently checked arithmetic and
  payload bind `|Gamma|=243`, `|Q0|=1,469,664`,
  `|Delta0|=|D_all|=357,128,352`, the `2916*504` Q0 order proof, 6,318
  Cayley edges, 104 action loops, 19 Q0 lifts, selected records
  `[1,3,6,9]`, closure order 243, matching upper/image orders, and all exact
  normal-closure Booleans and task157ee digests.
- **Bridge — PASS.**  Image order is 357,128,352 and kernel order is 1.
  Seven blocks, eleven typed occurrences, the ten-to-eleven and inverse
  maps, four marked inverse replays, all block/slot/context/type/sign
  bindings, and their internal order arithmetic agree.  The independently
  recomputed occurrence and 6,441-relator replay digests remain
  `040ab853535db8aad06fba295adf8b59bb1cd77435e7c64a1edcc34cdacb4cd7`
  and
  `613b08a923d14571bdd1b898e45b951a7fa61ca196dae64c07a7636b175d306f`.
- **Evaluator ABI — PASS.**  Bridge, evaluator, and task176 share typed
  coordinate digest
  `9f9c081e9653d6e141e4d6d231e2d6db9526850b7ccd33c0859d13825f3fa83c`;
  the v188 schema/callable, `load_runtime`, relator-row digest, and five
  width-40 plus five width-154 coordinates agree.
- **False witness claims — PASS.**  `cofinal_lift`, `fake`, and
  `Ihara_witness` are actual Boolean false values.
- **Corrected non-resource equality — PASS.**  The stronger comparison keeps
  the entire resume transcript and is byte-identical at the corrected
  31,016,535-byte digest above.

Reply327 explicitly found `FURTHER BUNDLE BLOCKERS: NONE`.  The sole former
blocker is now removed by task330's corrected expected reference, so there is
no remaining reason to reject the five-member authority bundle.

## 3. Scope and accounting

```text
AUTHORITY BUNDLE V2:           PASS / UNEXECUTED
A4 INPUT-AUTHORITY MILESTONE:  ELIGIBLE 1/3
A4 CONSUMER / PRODUCTION:      REJECTED / UNEXECUTED
LIFT / FAKE / IHARA:           NONE
```

This advances only v220 A4's authenticated input-authority milestone from
0/3 to 1/3.  Task323's A4/v2 implementation rejection, unconditional local-
evaluator/checker stops, unimplemented closure/K/anchor, and all later
witness obligations remain untouched.

`TASK330_R07_TASK327_AUTHORITY_NORMALIZATION_ERRATUM_COMPLETE`
